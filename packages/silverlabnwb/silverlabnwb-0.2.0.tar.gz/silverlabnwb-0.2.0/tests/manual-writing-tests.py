import os

import pytest

from silverlabnwb import NwbFile

DATA_PATH = os.environ.get('SILVERLAB_DATA_DIR', '')


@pytest.mark.skipif(
    not os.path.isdir(DATA_PATH),
    reason="raw data folder '{}' not present".format(DATA_PATH))
def test_all_funct_acq_writing():
    print("Searching for files")
    for subdirs in os.walk(DATA_PATH):
        import_folder_name = subdirs[0].split("\\")[-1]
        print("... in " + import_folder_name)
        if import_folder_name.startswith('sample') and not import_folder_name.endswith('VidRec'):
        # if import_folder_name.endswith('21 FunctAcq'):
            print("writing " + import_folder_name)
            with NwbFile(DATA_PATH + "\\nwb2\\" + import_folder_name.split(' ')[0] + ".nwb", mode='w') as nwb:
                nwb.import_labview_folder(subdirs[0])

    print("done with all.")


if __name__ == '__main__':
    print("Looking at folders in "+DATA_PATH)
    test_all_funct_acq_writing()
