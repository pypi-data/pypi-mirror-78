FROM fedora:30

RUN dnf install --assumeyes https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm \
  && dnf install --assumeyes findutils ffmpeg perl-Image-ExifTool \
  && dnf clean all

RUN pip3 install pytest pytest-sugar pytest-cov pytest-xdist \
  && pip3 install cryptography file-magic requests termcolor dnspython \
  && rm -rf /root/.cache
