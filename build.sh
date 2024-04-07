sysarch=$(uname -m)
arch=${1:-$sysarch}

cc -shared -fPIC -o bandwidth.dylib bandwidth.c && \
    rm -fr dist/* && \
    pyinstaller --target-arch $arch --noconfirm -i assets/AppIcon.icns -w -s Netivity.py && \
    rm -fr dist/Netivity && \
    ln -s /Applications dist/ && \
    hdiutil create -volname Netivity -ov -format UDZO -srcfolder ./dist ./dist/Netivity.dmg