FROM archlinux/base

RUN pacman -Syu --noconfirm \
  && pacman -S --noconfirm base-devel python python-pip ffmpeg perl-image-exiftool \
  && pacman -Scc --noconfirm \
  && ln -s /usr/bin/vendor_perl/exiftool /usr/bin/exiftool

RUN pip install pytest pytest-sugar pytest-cov pytest-xdist \
  && pip install cryptography file-magic requests termcolor dnspython \
  && rm -rf /root/.cache
