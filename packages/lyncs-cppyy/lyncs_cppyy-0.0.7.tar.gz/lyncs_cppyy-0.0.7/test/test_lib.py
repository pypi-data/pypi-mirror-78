import pytest
import tempfile
from mesonbuild import mesonmain
from lyncs_cppyy import Lib, cppdef, gbl


def build_meson(sourcedir):
    builddir = tempfile.mkdtemp()
    assert (
        mesonmain.run(
            [
                "setup",
                "--prefix",
                builddir,
                "--libdir",
                builddir + "/lib",
                builddir,
                sourcedir,
            ],
            "meson",
        )
        == 0
    )
    assert mesonmain.run(["compile", "-C", builddir], "meson") == 0
    assert mesonmain.run(["install", "-C", builddir], "meson") == 0
    return builddir


def test_cnumbers():
    path = build_meson("test/cnumbers")
    cnumbers = Lib(
        header="numbers.h",
        library="libnumbers.so",
        c_include=True,
        check=["zero", "one"],
        path=path,
    )
    assert cnumbers.zero() == 0
    assert cnumbers.one() == 1
    assert cnumbers.ZERO == 0
    assert cnumbers.ONE == 1

    # Cppyy cannot access macros.
    with pytest.raises(AttributeError):
        gbl.ZERO

    with pytest.raises(AttributeError):
        cnumbers.TWO

    with pytest.raises(RuntimeError):
        cnumbers.load()

    cnumbers.GLOBAL = 5
    assert cnumbers.GLOBAL == 5
    assert getattr(cnumbers, "global")() == 5

    cppnumbers = Lib(
        header="numbers.hpp",
        path=path,
        namespace="numbers",
        include=path + "/include",  # Not needed
        library=Lib(),  # Not needed
        redefined={"uno": "one", "GBL": "gbl"},
    )

    assert cppnumbers.zero["int"]() == 0
    assert cppnumbers.one["long"]() == 1
    assert cppnumbers.uno["long"]() == 1

    assert cppnumbers.ONE == 1

    cppnumbers.GBL = 1
    assert getattr(cppnumbers, "global")["int"]() == 1

    cppnumbers.GLOBAL = 1
    assert getattr(cnumbers, "global")() == 1


def test_errors():
    with pytest.raises(TypeError):
        Lib(header=[10])

    with pytest.raises(RuntimeError):
        Lib(check="foo").load()

    with pytest.raises(ValueError):
        Lib().get_macro("FOO")
