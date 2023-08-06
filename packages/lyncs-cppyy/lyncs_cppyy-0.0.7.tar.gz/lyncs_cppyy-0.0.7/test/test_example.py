def test_zlib():
    from lyncs_cppyy import Lib

    zlib = Lib(header="zlib.h", library="libz")
    assert zlib.zlibVersion() == zlib.ZLIB_VERSION
