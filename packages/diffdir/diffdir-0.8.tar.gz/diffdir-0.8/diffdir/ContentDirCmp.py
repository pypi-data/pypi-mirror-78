import os
from os.path import join
from filecmp import dircmp, cmpfiles


class ContentDirCmp(dircmp):
    def my_phase3(self):
        self.same_files, self.diff_files, self.funny_files = cmpfiles(
            self.left,
            self.right,
            self.common_files,
            shallow=False,  # shallow = False to make sure we will check file contents
        )

    def my_phase4(self):
        self.subdirs = {}
        for x in self.common_dirs:
            a_x = join(self.left, x)
            b_x = join(self.right, x)
            self.subdirs[x] = ContentDirCmp(a_x, b_x, self.ignore, self.hide)

    def get_diff_info(self):
        ret = []
        ret.append((join(self.left, item) for item in self.left_only))
        ret.append((join(self.right, item) for item in self.right_only))
        ret.append((join(self.left, item) for item in self.diff_files))
        ret.append((join(self.left, item) for item in self.funny_files))
        return ret  # left_only, right_only, diff_files, funny_files

    methodmap = dict(
        subdirs=my_phase4,
        same_files=my_phase3,
        diff_files=my_phase3,
        funny_files=my_phase3,
        common_dirs=dircmp.phase2,
        common_files=dircmp.phase2,
        common_funny=dircmp.phase2,
        common=dircmp.phase1,
        left_only=dircmp.phase1,
        right_only=dircmp.phase1,
        left_list=dircmp.phase0,
        right_list=dircmp.phase0,
    )

    def work(self):
        yield self.get_diff_info()
        for sd in self.subdirs.values():
            yield from sd.work()


if __name__ == "__main__":
    for lx, rx, dx, fx in ContentDirCmp("./foo", "./bar/foo").work():
        for item in dx:
            print(item)
