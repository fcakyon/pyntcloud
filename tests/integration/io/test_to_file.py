import pytest

from pyntcloud import PyntCloud

from test_from_file import assert_points_xyz, assert_points_color, assert_mesh


@pytest.mark.parametrize("extension,color,mesh,comments", [
    (".ply", True, True, False),
    ("_ascii.ply", True, True, True),
    (".npz", True, True, False),
    (".obj", False, True, False),
    (".bin", False, False, False)
])
def test_to_file(tmpdir, diamond, extension, color, mesh, comments):
    extra_write_args = {}
    if mesh:
        extra_write_args["also_save"] = ["mesh"]
    if comments:
        extra_write_args["comments"] = ["PyntCloud is cool"]
    if extension == ".ply":
        extra_write_args["as_text"] = False
    if extension == "_ascii.ply":
        extra_write_args["as_text"] = True

    diamond.to_file(str(tmpdir.join("written{}".format(extension))), **extra_write_args)

    written_file = PyntCloud.from_file(str(tmpdir.join("written{}".format(extension))))

    assert_points_xyz(written_file)
    if color:
        assert_points_color(written_file)
    if mesh:
        assert_mesh(written_file)
    if comments:
        assert written_file.comments == ["PyntCloud is cool"]

def test_to_bin_raises_ValueError_if_invalid_kwargs(tmpdir, diamond):
    with pytest.raises(ValueError):
        diamond.to_file(str(tmpdir.join("written.bin")), also_save=["mesh"])