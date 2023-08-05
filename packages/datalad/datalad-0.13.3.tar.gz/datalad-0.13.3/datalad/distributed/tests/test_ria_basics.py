# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import logging
from datalad.api import (
    Dataset,
    clone,
)
from datalad.utils import Path
from datalad.tests.utils import (
    assert_equal,
    assert_in,
    assert_not_in,
    assert_raises,
    assert_repo_status,
    assert_status,
    assert_true,
    has_symlink_capability,
    SkipTest,
    known_failure_windows,
    skip_if_no_network,
    skip_ssh,
    slow,
    swallow_logs,
    turtle,
    with_tempfile
)
from datalad.distributed.ora_remote import (
    LocalIO,
    SSHRemoteIO
)
from datalad.support.exceptions import (
    CommandError,
    IncompleteResultsError
)
from datalad.distributed.tests.ria_utils import (
    get_all_files,
    populate_dataset,
    common_init_opts
)
from datalad.customremotes.ria_utils import (
    create_store,
    create_ds_in_store,
    get_layout_locations
)


# Note, that exceptions to test for are generally CommandError since we are
# talking to the special remote via annex.

@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
@with_tempfile
def _test_initremote_basic(host, ds_path, store, link):

    ds_path = Path(ds_path)
    store = Path(store)
    link = Path(link)
    ds = Dataset(ds_path).create()
    populate_dataset(ds)
    ds.save()

    if host:
        url = "ria+ssh://{host}{path}".format(host=host,
                                              path=store)
    else:
        url = "ria+{}".format(store.as_uri())
    init_opts = common_init_opts + ['url={}'.format(url)]

    # fails on non-existing storage location
    assert_raises(CommandError,
                  ds.repo.init_remote, 'ria-remote', options=init_opts)
    # Doesn't actually create a remote if it fails
    assert_not_in('ria-remote',
                  [cfg['name']
                   for uuid, cfg in ds.repo.get_special_remotes().items()]
                  )

    # fails on non-RIA URL
    assert_raises(CommandError, ds.repo.init_remote, 'ria-remote',
                  options=common_init_opts + ['url={}'.format(store.as_uri())]
                  )
    # Doesn't actually create a remote if it fails
    assert_not_in('ria-remote',
                  [cfg['name']
                   for uuid, cfg in ds.repo.get_special_remotes().items()]
                  )

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    create_store(io, store, '1')
    # still fails, since ds isn't setup in the store
    assert_raises(CommandError,
                  ds.repo.init_remote, 'ria-remote', options=init_opts)
    # Doesn't actually create a remote if it fails
    assert_not_in('ria-remote',
                  [cfg['name']
                   for uuid, cfg in ds.repo.get_special_remotes().items()]
                  )
    # set up the dataset as well
    create_ds_in_store(io, store, ds.id, '2', '1')
    # now should work
    ds.repo.init_remote('ria-remote', options=init_opts)
    assert_in('ria-remote',
              [cfg['name']
               for uuid, cfg in ds.repo.get_special_remotes().items()]
              )
    assert_repo_status(ds.path)
    # git-annex:remote.log should have:
    #   - url
    #   - common_init_opts
    #   - archive_id (which equals ds id)
    remote_log = ds.repo.call_git(['cat-file', 'blob', 'git-annex:remote.log'])
    assert_in("url={}".format(url), remote_log)
    [assert_in(c, remote_log) for c in common_init_opts]
    assert_in("archive-id={}".format(ds.id), remote_log)

    # re-configure with invalid URL should fail:
    assert_raises(CommandError,
                  ds.repo.call_git,
                  ['annex', 'enableremote', 'ria-remote'] + common_init_opts +
                  ['url=ria+file:///non-existing']
                  )
    # but re-configure with valid URL should work
    if has_symlink_capability():
        link.symlink_to(store)
        new_url = 'ria+{}'.format(link.as_uri())
        ds.repo.call_git(['annex', 'enableremote', 'ria-remote'] +
                         common_init_opts +
                         ['url={}'.format(new_url)])
        # git-annex:remote.log should have:
        #   - url
        #   - common_init_opts
        #   - archive_id (which equals ds id)
        remote_log = ds.repo.call_git(['cat-file', 'blob',
                                       'git-annex:remote.log'])
        assert_in("url={}".format(new_url), remote_log)
        [assert_in(c, remote_log) for c in common_init_opts]
        assert_in("archive-id={}".format(ds.id), remote_log)

    # TODO: - check output of failures to verify it's failing the right way
    #       - might require to run initremote directly to get the output


def test_initremote_basic():

    # TODO: Skipped due to gh-4436
    yield known_failure_windows(skip_ssh(_test_initremote_basic)), \
          'datalad-test'
    yield _test_initremote_basic, None


@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
def _test_initremote_rewrite(host, ds_path, store):

    # rudimentary repetition of test_initremote_basic, but
    # with url.<base>.insteadOf config, which should not only
    # be respected, but lead to the rewritten URL stored in
    # git-annex:remote.log

    ds_path = Path(ds_path)
    store = Path(store)
    ds = Dataset(ds_path).create()
    populate_dataset(ds)
    ds.save()
    assert_repo_status(ds.path)

    url = "mystore:"
    init_opts = common_init_opts + ['url={}'.format(url)]

    if host:
        replacement = "ria+ssh://{host}{path}".format(host=host,
                                                      path=store)
    else:
        replacement = "ria+{}".format(store.as_uri())

    ds.config.set("url.{}.insteadOf".format(replacement), url, where='local')

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    create_store(io, store, '1')
    create_ds_in_store(io, store, ds.id, '2', '1')

    # run initremote and check what's stored:
    ds.repo.init_remote('ria-remote', options=init_opts)
    assert_in('ria-remote',
              [cfg['name']
               for uuid, cfg in ds.repo.get_special_remotes().items()]
              )
    # git-annex:remote.log should have:
    #   - rewritten url
    #   - common_init_opts
    #   - archive_id (which equals ds id)
    remote_log = ds.repo.call_git(['cat-file', 'blob', 'git-annex:remote.log'])
    assert_in("url={}".format(replacement), remote_log)
    [assert_in(c, remote_log) for c in common_init_opts]
    assert_in("archive-id={}".format(ds.id), remote_log)


def test_initremote_rewrite():
    # TODO: Skipped due to gh-4436
    yield known_failure_windows(skip_ssh(_test_initremote_rewrite)), \
          'datalad-test'
    yield _test_initremote_rewrite, None


@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
@with_tempfile
def _test_remote_layout(host, dspath, store, archiv_store):

    dspath = Path(dspath)
    store = Path(store)
    archiv_store = Path(archiv_store)
    ds = Dataset(dspath).create()
    populate_dataset(ds)
    ds.save()
    assert_repo_status(ds.path)

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    if host:
        store_url = "ria+ssh://{host}{path}".format(host=host,
                                                    path=store)
        arch_url = "ria+ssh://{host}{path}".format(host=host,
                                                   path=archiv_store)
    else:
        store_url = "ria+{}".format(store.as_uri())
        arch_url = "ria+{}".format(archiv_store.as_uri())

    create_store(io, store, '1')

    # TODO: Re-establish test for version 1
    # version 2: dirhash
    create_ds_in_store(io, store, ds.id, '2', '1')

    # add special remote
    init_opts = common_init_opts + ['url={}'.format(store_url)]
    ds.repo.init_remote('store', options=init_opts)

    # copy files into the RIA store
    ds.repo.copy_to('.', 'store')

    # we should see the exact same annex object tree
    dsgit_dir, archive_dir, dsobj_dir = \
        get_layout_locations(1, store, ds.id)
    store_objects = get_all_files(dsobj_dir)
    local_objects = get_all_files(ds.pathobj / '.git' / 'annex' / 'objects')
    assert_equal(len(store_objects), 2)

    if not ds.repo.is_managed_branch():
        # with managed branches the local repo uses hashdirlower instead
        # TODO: However, with dataset layout version 1 this should therefore
        #       work on adjusted branch the same way
        # TODO: Wonder whether export-archive-ora should account for that and
        #       rehash according to target layout.
        assert_equal(sorted([p for p in store_objects]),
                     sorted([p for p in local_objects])
                     )

        # we can simply pack up the content of the remote into a
        # 7z archive and place it in the right location to get a functional
        # archive remote
        whereis = ds.repo.whereis('one.txt')
        dsgit_dir, archive_dir, dsobj_dir = \
            get_layout_locations(1, archiv_store, ds.id)
        ds.export_archive_ora(archive_dir / 'archive.7z')
        init_opts = common_init_opts + ['url={}'.format(arch_url)]
        ds.repo.init_remote('archive', options=init_opts)
        # now fsck the new remote to get the new special remote indexed
        ds.repo.fsck(remote='archive', fast=True)
        assert_equal(len(ds.repo.whereis('one.txt')), len(whereis) + 1)


@slow  # 12sec + ? on travis
def test_remote_layout():
    # TODO: Skipped due to gh-4436
    yield known_failure_windows(skip_ssh(_test_remote_layout)), 'datalad-test'
    yield _test_remote_layout, None


@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
def _test_version_check(host, dspath, store):

    dspath = Path(dspath)
    store = Path(store)

    ds = Dataset(dspath).create()
    populate_dataset(ds)
    ds.save()
    assert_repo_status(ds.path)

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    if host:
        store_url = "ria+ssh://{host}{path}".format(host=host,
                                                    path=store)
    else:
        store_url = "ria+{}".format(store.as_uri())

    create_store(io, store, '1')

    # TODO: Re-establish test for version 1
    # version 2: dirhash
    create_ds_in_store(io, store, ds.id, '2', '1')

    # add special remote
    init_opts = common_init_opts + ['url={}'.format(store_url)]
    ds.repo.init_remote('store', options=init_opts)
    ds.repo.copy_to('.', 'store')

    # check version files
    remote_ds_tree_version_file = store / 'ria-layout-version'
    dsgit_dir, archive_dir, dsobj_dir = \
        get_layout_locations(1, store, ds.id)
    remote_obj_tree_version_file = dsgit_dir / 'ria-layout-version'

    assert_true(remote_ds_tree_version_file.exists())
    assert_true(remote_obj_tree_version_file.exists())

    with open(str(remote_ds_tree_version_file), 'r') as f:
        assert_equal(f.read().strip(), '1')
    with open(str(remote_obj_tree_version_file), 'r') as f:
        assert_equal(f.read().strip(), '2')

    # Accessing the remote should not yield any output regarding versioning,
    # since it's the "correct" version. Note that "fsck" is an arbitrary choice.
    # We need just something to talk to the special remote.
    with swallow_logs(new_level=logging.INFO) as cml:
        ds.repo.fsck(remote='store', fast=True)
        # TODO: For some reason didn't get cml.assert_logged to assert
        #       "nothing was logged"
        assert not cml.out

    # Now fake-change the version
    with open(str(remote_obj_tree_version_file), 'w') as f:
        f.write('X\n')

    # Now we should see a message about it
    with swallow_logs(new_level=logging.INFO) as cml:
        ds.repo.fsck(remote='store', fast=True)
        cml.assert_logged(level="INFO",
                          msg="Remote object tree reports version X",
                          regex=False)

    # reading still works:
    ds.drop('.')
    assert_status('ok', ds.get('.'))

    # but writing doesn't:
    with open(str(Path(ds.path) / 'new_file'), 'w') as f:
        f.write("arbitrary addition")
    ds.save(message="Add a new_file")

    # TODO: use self.annex.error in special remote and see whether we get an
    #       actual error result
    assert_raises(IncompleteResultsError,
                  ds.repo.copy_to, 'new_file', 'store')

    # However, we can force it by configuration
    ds.config.add("annex.ora-remote.store.force-write", "true", where='local')
    ds.repo.copy_to('new_file', 'store')


@slow  # 17sec + ? on travis
def test_version_check():
    # TODO: Skipped due to gh-4436
    yield known_failure_windows(skip_ssh(_test_version_check)), 'datalad-test'
    yield _test_version_check, None


@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
def _test_gitannex(host, store, dspath):

    from datalad.cmd import (
        GitRunner,
        WitlessRunner
    )
    store = Path(store)

    dspath = Path(dspath)
    store = Path(store)

    ds = Dataset(dspath).create()

    if ds.repo.is_managed_branch():
        # git-annex-testremote is way too slow on crippled FS.
        # Use is_managed_branch() as a proxy and skip only here
        # instead of in a decorator
        raise SkipTest("Test too slow on crippled FS")

    populate_dataset(ds)
    ds.save()
    assert_repo_status(ds.path)

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    if host:
        store_url = "ria+ssh://{host}{path}".format(host=host,
                                                    path=store)
    else:
        store_url = "ria+{}".format(store.as_uri())

    create_store(io, store, '1')

    # TODO: Re-establish test for version 1
    # version 2: dirhash
    create_ds_in_store(io, store, ds.id, '2', '1')

    # add special remote
    init_opts = common_init_opts + ['url={}'.format(store_url)]
    ds.repo.init_remote('store', options=init_opts)

    from datalad.support.external_versions import external_versions
    if '8.20200330' < external_versions['cmd:annex'] < '8.20200624':
        # https://git-annex.branchable.com/bugs/testremote_breeds_way_too_many_instances_of_the_externals_remote/?updated
        raise SkipTest(
            "git-annex might lead to overwhelming number of external "
            "special remote instances")

    # run git-annex-testremote
    # note, that we don't want to capture output. If something goes wrong we
    # want to see it in test build's output log.
    WitlessRunner(cwd=dspath, env=GitRunner.get_git_environ_adjusted()).run(
        ['git', 'annex', 'testremote', 'store']
    )


@turtle
@known_failure_windows # TODO: Skipped due to gh-4436
@skip_ssh
def test_gitannex_ssh():
    _test_gitannex('datalad-test')


@slow  # 41sec on travis
def test_gitannex_local():
    _test_gitannex(None)


@known_failure_windows  # see gh-4469
@with_tempfile
@with_tempfile
def _test_binary_data(host, store, dspath):
    # make sure, special remote deals with binary data and doesn't
    # accidentally involve any decode/encode etc.

    dspath = Path(dspath)
    store = Path(store)

    url = "https://github.com/datalad/example-dicom-functional/blob/master/dicoms/MR.1.3.46.670589.11.38317.5.0.4476.2014042516042547586"
    file = "dicomfile"
    ds = Dataset(dspath).create()
    ds.download_url(url, path=file, message="Add DICOM file from github")
    assert_repo_status(ds.path)

    # set up store:
    io = SSHRemoteIO(host) if host else LocalIO()
    if host:
        store_url = "ria+ssh://{host}{path}".format(host=host,
                                                    path=store)
    else:
        store_url = "ria+{}".format(store.as_uri())

    create_store(io, store, '1')
    create_ds_in_store(io, store, ds.id, '2', '1')

    # add special remote
    init_opts = common_init_opts + ['url={}'.format(store_url)]
    ds.repo.init_remote('store', options=init_opts)

    # actual data transfer (both directions)
    # Note, that we intentionally call annex commands instead of
    # datalad-publish/-get here. We are testing an annex-special-remote.

    store_uuid = ds.siblings(name='store',
                             return_type='item-or-list')['annex-uuid']
    here_uuid = ds.siblings(name='here',
                            return_type='item-or-list')['annex-uuid']

    known_sources = ds.repo.whereis(str(file))
    assert_in(here_uuid, known_sources)
    assert_not_in(store_uuid, known_sources)
    ds.repo.call_git(['annex', 'move', str(file), '--to', 'store'])
    known_sources = ds.repo.whereis(str(file))
    assert_not_in(here_uuid, known_sources)
    assert_in(store_uuid, known_sources)
    ds.repo.call_git(['annex', 'get', str(file), '--from', 'store'])
    known_sources = ds.repo.whereis(str(file))
    assert_in(here_uuid, known_sources)
    assert_in(store_uuid, known_sources)


def test_binary_data():
    # TODO: Skipped due to gh-4436
    yield known_failure_windows(skip_ssh(_test_binary_data)), 'datalad-test'
    yield skip_if_no_network(_test_binary_data), None
