import ezconfig
import os
import pyfakefs.fake_filesystem as fake_fs


conf_basename = "test_config"

dir_conf_file = os.path.abspath(os.path.join(os.getcwd(), conf_basename))
dev_conf_file = os.path.abspath("../../conf/{}".format(conf_basename))
usr_conf_file = os.path.abspath(os.path.expanduser("~/{}".format(conf_basename)))
git_dir_sentinal = os.path.abspath("../../.git")

ofind_dir_config_file = lambda : os.path.join(os.getcwd(), conf_basename)
find_dev_config_file = lambda : ezconfig.get_filename_relative_to_sentinal(os.getcwd(),
                                                                           ".git", conf_basename)
find_usr_config_file = lambda : ezconfig.get_userdir_filename(conf_basename)

ezconfig_find_all_config_files = lambda : (find_dir_config_file(),
                                           find_dev_config_file(),
                                           find_usr_config_file())
ezconfig_find_config = lambda : ezconfig.get_best_filename(ezconfig_find_all_config_files())

# class MyTest(fake_filesystem_unittest.TestCase):
#     def setUp(self):
#         self.setUpPyfakefs()

#     def tearDown(self):
#         # It is no longer necessary to add self.tearDownPyfakefs()
#         pass

#     def my_fakefs_test(self):
#         # "fs" is the reference to the fake file system
#         fs = fake_fs.FakeFilesystem()
#         fs.CreateFile('/var/data/xx1.txt')
#         assert os.path.exists('/var/data/xx1.txt')

# def is_same_fn(fn1, fn2):
#     f = lambda fn: os.path.abspath(os.path.expanduser(fn))
#     return f(fn1) == f(fn2)

# def test_fake_filesystem():
#     fs = fake_fs.FakeFilesystem()

#     fs.CreateFile(dir_conf_file)
#     fs.CreateFile(dev_conf_file)
#     fs.CreateFile(usr_conf_file)

#     abs_dir_conf_file = os.path.abspath(dev_conf_file)
#     abs_dev_conf_file = os.path.abspath(dir_conf_file)
#     abs_usr_conf_file = os.path.abspath(usr_conf_file)

#     assert os.path.isfile(dir_conf_file)
#     assert os.path.isfile(dev_conf_file)
#     assert os.path.isfile(usr_conf_file)
#     return


# def test_ezconfig_sentinal_conf_search():

#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(dev_conf_file)

#     dev_conf = ezconfig.get_filename_relative_to_sentinal(os.getcwd(), ".git",
#                                                           conf_basename)

#     pdb.set_trace()
#     assert is_same_fn(dev_conf, dev_conf_file)

# def test_usr_config_file_only():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(usr_conf_file)
#     assert is_same_fn(ezconfig_find_config(), usr_conf_file)
#     return

# def test_dir_config_file_only():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(dir_conf_file)
#     import pdb
#     pdb.set_trace()
#     assert is_same_fn(ezconfig_find_config(), dir_conf_file)
#     return

# def test_dev_config_only():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(dev_conf_file)
#     assert is_same_fn(ezconfig_find_config(), dev_conf_file)
#     return


# def test_config_preference_dev():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(dir_conf_file)
#     fs.CreateFile(dev_conf_file)
#     assert is_same_fn(ezconfig_find_config(), dir_conf_file)
#     return

# def test_config_preference_dev2():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(dir_conf_file)
#     fs.CreateFile(dev_conf_file)
#     fs.CreateFile(usr_conf_file)
#     assert is_same_fn(ezconfig_find_config(), dir_conf_file)

#     return

# def test_config_preference_deployed():
#     fs = fake_fs.FakeFilesystem()
#     fs.CreateFile(usr_conf_file)
#     assert is_same_fn(ezconfig_find_config(), usr_conf_file)
#     return
