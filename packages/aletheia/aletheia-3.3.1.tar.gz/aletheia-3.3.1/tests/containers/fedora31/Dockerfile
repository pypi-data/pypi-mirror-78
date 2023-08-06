FROM fedora:31

RUN dnf install --assumeyes https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm \
  && dnf install --assumeyes findutils ffmpeg perl-Image-ExifTool python \
  && dnf clean all

RUN pip install pytest pytest-sugar pytest-cov pytest-xdist \
  && pip install cryptography file-magic requests termcolor dnspython \
  && rm -rf /root/.cache
