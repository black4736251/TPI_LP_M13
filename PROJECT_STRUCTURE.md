# Estrutura do projecto 📁

Voltar à [página principal](https://github.com/black4736251/TPI_LP_M13)

```
.
├── builds
│   ├── main.build
│   │   ├── build_definitions.h
│   │   ├── __bytecode.const
│   │   ├── __constants.bin
│   │   ├── __constants.c
│   │   ├── __constants.const
│   │   ├── __constants_data.c
│   │   ├── __constants_data.o
│   │   ├── __constants.h
│   │   ├── __constants.o
│   │   ├── __constants.txt
│   │   ├── __helpers.c
│   │   ├── __helpers.h
│   │   ├── __helpers.o
│   │   ├── @link_input.txt
│   │   ├── __loader.c
│   │   ├── __loader.o
│   │   ├── module.__main__.c
│   │   ├── module.__main__.const
│   │   ├── module.__main__.o
│   │   ├── module.PySide6.c
│   │   ├── module.PySide6.const
│   │   ├── module.PySide6.o
│   │   ├── module.PySide6-postLoad.c
│   │   ├── module.PySide6-postLoad.const
│   │   ├── module.PySide6-postLoad.o
│   │   ├── module.PySide6.QtCore-postLoad.c
│   │   ├── module.PySide6.QtCore-postLoad.const
│   │   ├── module.PySide6.QtCore-postLoad.o
│   │   ├── module.PySide6.support.c
│   │   ├── module.PySide6.support.const
│   │   ├── module.PySide6.support.deprecated.c
│   │   ├── module.PySide6.support.deprecated.const
│   │   ├── module.PySide6.support.deprecated.o
│   │   ├── module.PySide6.support.o
│   │   ├── module.shiboken6.c
│   │   ├── module.shiboken6.const
│   │   ├── module.shiboken6.o
│   │   ├── module.sources.c
│   │   ├── module.sources.cart.c
│   │   ├── module.sources.cart.const
│   │   ├── module.sources.cart.o
│   │   ├── module.sources.config.c
│   │   ├── module.sources.config.const
│   │   ├── module.sources.config.o
│   │   ├── module.sources.const
│   │   ├── module.sources.database.c
│   │   ├── module.sources.database.const
│   │   ├── module.sources.database.o
│   │   ├── module.sources.login.c
│   │   ├── module.sources.login.const
│   │   ├── module.sources.login.o
│   │   ├── module.sources.o
│   │   ├── module.sources.shop.c
│   │   ├── module.sources.shop.const
│   │   ├── module.sources.shop.o
│   │   ├── module.sources.sound_manager.c
│   │   ├── module.sources.sound_manager.const
│   │   ├── module.sources.sound_manager.o
│   │   ├── module.sources.start.c
│   │   ├── module.sources.start.const
│   │   ├── module.sources.start.o
│   │   ├── module.sources.stock.c
│   │   ├── module.sources.stock.const
│   │   ├── module.sources.stock.o
│   │   ├── module.sources.utils.c
│   │   ├── module.sources.utils.const
│   │   ├── module.sources.utils.o
│   │   ├── scons-debug.py
│   │   ├── scons-debug.sh
│   │   ├── scons-report.txt
│   │   └── static_src
│   │       ├── CompiledFunctionType.c -> ~/venv/lib/python3.13/site-packages/nuitka/build/static_src/CompiledFunctionType.c
│   │       ├── CompiledFunctionType.o
│   │       ├── MainProgram.c -> ~/venv/lib/python3.13/site-packages/nuitka/build/static_src/MainProgram.c
│   │       └── MainProgram.o
│   └── main.dist
│       ├── _bz2.so
│       ├── _codecs_cn.so
│       ├── _codecs_hk.so
│       ├── _codecs_iso2022.so
│       ├── _codecs_jp.so
│       ├── _codecs_kr.so
│       ├── _codecs_tw.so
│       ├── _contextvars.so
│       ├── databases
│       │   └── database.db
│       ├── _decimal.so
│       ├── _hashlib.so
│       ├── images
│       │   ├── program
│       │   │   ├── bugatti_bolide.png
│       │   │   ├── cart.png
│       │   │   ├── eye.png
│       │   │   ├── mazda_mx-5.png
│       │   │   └── nissan_gt-r.png
│       │   └── readme
│       │       ├── cart.png
│       │       ├── login.png
│       │       ├── shop.png
│       │       └── stock.png
│       ├── libavcodec.so.61
│       ├── libavformat.so.61
│       ├── libavutil.so.59
│       ├── libbz2.so.1.0
│       ├── libcrypto.so.3
│       ├── libexpat.so.1
│       ├── libicudata.so.73
│       ├── libicui18n.so.73
│       ├── libicuuc.so.73
│       ├── liblzma.so.5
│       ├── libpyside6.abi3.so.6.11
│       ├── libQt6Concurrent.so.6
│       ├── libQt6Core.so.6
│       ├── libQt6DBus.so.6
│       ├── libQt6EglFSDeviceIntegration.so.6
│       ├── libQt6EglFsKmsSupport.so.6
│       ├── libQt6FFmpegStub-crypto.so.3
│       ├── libQt6FFmpegStub-ssl.so.3
│       ├── libQt6FFmpegStub-va-drm.so.2
│       ├── libQt6FFmpegStub-va.so.2
│       ├── libQt6FFmpegStub-va-x11.so.2
│       ├── libQt6Gui.so.6
│       ├── libQt6Multimedia.so.6
│       ├── libQt6Network.so.6
│       ├── libQt6OpenGL.so.6
│       ├── libQt6Pdf.so.6
│       ├── libQt6PrintSupport.so.6
│       ├── libQt6QmlMeta.so.6
│       ├── libQt6QmlModels.so.6
│       ├── libQt6Qml.so.6
│       ├── libQt6QmlWorkerScript.so.6
│       ├── libQt6Quick.so.6
│       ├── libQt6Svg.so.6
│       ├── libQt6WaylandClient.so.6
│       ├── libQt6Widgets.so.6
│       ├── libQt6WlShellIntegration.so.6
│       ├── libQt6XcbQpa.so.6
│       ├── libshiboken6.abi3.so.6.11
│       ├── libsqlite3.so.0
│       ├── libssl.so.3
│       ├── libswresample.so.5
│       ├── libswscale.so.8
│       ├── libzstd.so.1
│       ├── _lzma.so
│       ├── main.bin
│       ├── _multibytecodec.so
│       ├── PySide6
│       │   ├── QtCore.so
│       │   ├── QtGui.so
│       │   ├── QtMultimedia.so
│       │   ├── QtNetwork.so
│       │   ├── qt-plugins
│       │   │   ├── egldeviceintegrations
│       │   │   │   ├── libqeglfs-emu-integration.so
│       │   │   │   ├── libqeglfs-kms-egldevice-integration.so
│       │   │   │   ├── libqeglfs-kms-integration.so
│       │   │   │   └── libqeglfs-x11-integration.so
│       │   │   ├── iconengines
│       │   │   │   └── libqsvgicon.so
│       │   │   ├── imageformats
│       │   │   │   ├── libqgif.so
│       │   │   │   ├── libqicns.so
│       │   │   │   ├── libqico.so
│       │   │   │   ├── libqjpeg.so
│       │   │   │   ├── libqpdf.so
│       │   │   │   ├── libqsvg.so
│       │   │   │   ├── libqtga.so
│       │   │   │   ├── libqtiff.so
│       │   │   │   ├── libqwbmp.so
│       │   │   │   └── libqwebp.so
│       │   │   ├── multimedia
│       │   │   │   └── libffmpegmediaplugin.so
│       │   │   ├── platforms
│       │   │   │   ├── libqeglfs.so
│       │   │   │   ├── libqlinuxfb.so
│       │   │   │   ├── libqminimalegl.so
│       │   │   │   ├── libqminimal.so
│       │   │   │   ├── libqoffscreen.so
│       │   │   │   ├── libqvkkhrdisplay.so
│       │   │   │   ├── libqvnc.so
│       │   │   │   ├── libqwayland.so
│       │   │   │   └── libqxcb.so
│       │   │   ├── platformthemes
│       │   │   │   ├── libqgtk3.so
│       │   │   │   └── libqxdgdesktopportal.so
│       │   │   ├── printsupport
│       │   │   │   └── libcupsprintersupport.so
│       │   │   ├── tls
│       │   │   │   ├── libqcertonlybackend.so
│       │   │   │   └── libqopensslbackend.so
│       │   │   ├── wayland-decoration-client
│       │   │   │   ├── libadwaita.so
│       │   │   │   └── libbradient.so
│       │   │   ├── wayland-graphics-integration-client
│       │   │   │   ├── libdmabuf-server.so
│       │   │   │   ├── libdrm-egl-server.so
│       │   │   │   ├── libqt-plugin-wayland-egl.so
│       │   │   │   ├── libshm-emulation-server.so
│       │   │   │   └── libvulkan-server.so
│       │   │   ├── wayland-shell-integration
│       │   │   │   ├── libfullscreen-shell-v1.so
│       │   │   │   ├── libivi-shell.so
│       │   │   │   ├── libqt-shell.so
│       │   │   │   ├── libwl-shell-plugin.so
│       │   │   │   └── libxdg-shell.so
│       │   │   └── xcbglintegrations
│       │   │       ├── libqxcb-egl-integration.so
│       │   │       └── libqxcb-glx-integration.so
│       │   └── QtWidgets.so
│       ├── reports
│       │   └── sales.csv
│       ├── shiboken6
│       │   └── Shiboken.so
│       ├── sounds
│       │   ├── click.mp3
│       │   ├── close.mp3
│       │   ├── information.mp3
│       │   ├── login.mp3
│       │   ├── purchase.mp3
│       │   ├── shop.mp3
│       │   ├── stock.mp3
│       │   └── warning.mp3
│       └── _sqlite3.so
├── build.sh
├── databases
│   └── database.db
├── images
│   ├── program
│   │   ├── bugatti_bolide.png
│   │   ├── cart.png
│   │   ├── eye.png
│   │   ├── mazda_mx-5.png
│   │   └── nissan_gt-r.png
│   └── readme
│       ├── cart.png
│       ├── login.png
│       ├── shop.png
│       └── stock.png
├── main.py
├── PROJECT_STRUCTURE.md
├── README.md
├── reports
│   └── sales.csv
├── requirements.txt
├── sounds
│   ├── click.mp3
│   ├── close.mp3
│   ├── information.mp3
│   ├── login.mp3
│   ├── purchase.mp3
│   ├── shop.mp3
│   ├── stock.mp3
│   └── warning.mp3
└── sources
    ├── cart.py
    ├── config.py
    ├── database.py
    ├── login.py
    ├── shop.py
    ├── sound_manager.py
    ├── start.py
    ├── stock.py
    └── utils.py
```
