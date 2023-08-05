// Copyright 2017 Global Phasing Ltd.
//
// Functions for transparent reading of gzipped files. Uses zlib.

#ifndef GEMMI_GZ_HPP_
#define GEMMI_GZ_HPP_
#include <cassert>
#include <cstdio>       // fseek, ftell, fread
#include <climits>      // INT_MAX
#include <memory>
#include <string>
#include <zlib.h>
#include "fail.hpp"     // fail
#include "fileutil.hpp" // file_open
#include "input.hpp"    // BasicInput
#include "util.hpp"     // iends_with

namespace gemmi {

// Throws if the size is not found or if it is suspicious.
// Anything outside of the arbitrary limits from 1 to 10x of the compressed
// size looks suspicious to us.
inline size_t estimate_uncompressed_size(const std::string& path) {
  fileptr_t f = file_open(path.c_str(), "rb");
  if (std::fseek(f.get(), -4, SEEK_END) != 0)
    fail("fseek() failed (empty file?): " + path);
  long pos = std::ftell(f.get());
  if (pos <= 0)
    fail("ftell() failed on " + path);
  size_t gzipped_size = pos + 4;
  unsigned char buf[4];
  if (std::fread(buf, 1, 4, f.get()) != 4)
    fail("Failed to read last 4 bytes of: " + path);
  unsigned orig_size = (buf[3] << 24) | (buf[2] << 16) | (buf[1] << 8) | buf[0];
  if (orig_size + 100 < gzipped_size || orig_size > 100 * gzipped_size)
    fail("Cannot determine uncompressed size of " + path +
         "\nWould it be " + std::to_string(gzipped_size) + " -> " +
         std::to_string(orig_size) + " bytes?");
  return orig_size;
}

inline size_t big_gzread(gzFile file, void* buf, size_t len) {
  // In zlib >= 1.2.9 we could use gzfread()
  // return gzfread(buf, len, 1, f) == 1;
  size_t read_bytes = 0;
  while (len > INT_MAX) {
    int ret = gzread(file, buf, INT_MAX);
    read_bytes += ret;
    if (ret != INT_MAX)
      return read_bytes;
    len -= INT_MAX;
    buf = (char*) buf + INT_MAX;
  }
  read_bytes += gzread(file, buf, (unsigned) len);
  return read_bytes;
}

class MaybeGzipped : public BasicInput {
public:
  struct GzStream {
    gzFile f;
    char* gets(char* line, int size) { return gzgets(f, line, size); }
    int getc() { return gzgetc(f); }
    bool read(void* buf, size_t len) { return big_gzread(f, buf, len) == len; }
  };

  explicit MaybeGzipped(const std::string& path)
    : BasicInput(path), memory_size_(0), file_(nullptr) {}
  ~MaybeGzipped() {
    if (file_)
#if ZLIB_VERNUM >= 0x1235
      gzclose_r(file_);
#else
      gzclose(file_);
#endif
  }

  size_t gzread_checked(void* buf, size_t len) {
    size_t read_bytes = big_gzread(file_, buf, len);
    if (read_bytes != len && !gzeof(file_)) {
      int errnum;
      std::string err_str = gzerror(file_, &errnum);
      if (errnum)
        fail("Error reading " + path() + ": " + err_str);
    }
    if (read_bytes > len)  // should never happen
      fail("Error reading " + path());
    return read_bytes;
  }

  bool is_compressed() const { return iends_with(path(), ".gz"); }
  std::string basepath() const {
    return is_compressed() ? path().substr(0, path().size() - 3) : path();
  }
  size_t memory_size() const { return memory_size_; }

  std::unique_ptr<char[]> memory() {
    if (!is_compressed())
      return BasicInput::memory();
    memory_size_ = estimate_uncompressed_size(path());
    open();
    if (memory_size_ > 3221225471)
      fail("For now gz files above 3 GiB uncompressed are not supported.");
    std::unique_ptr<char[]> mem(new char[memory_size_]);
    size_t read_bytes = gzread_checked(mem.get(), memory_size_);
    // if the file is shorter than the size from header, adjust memory_size_
    if (read_bytes < memory_size_) {
      memory_size_ = read_bytes;
    } else { // read_bytes == memory_size_
    // if the file is longer than the size from header, read in the rest
      int next_char;
      while (!gzeof(file_) && (next_char = gzgetc(file_)) != -1) {
        if (memory_size_ > 3221225471)
          fail("For now gz files above 3 GiB uncompressed are not supported.");
        gzungetc(next_char, file_);
        std::unique_ptr<char[]> mem2(new char[2 * memory_size_]);
        std::memcpy(mem2.get(), mem.get(), memory_size_);
        memory_size_ += gzread_checked(mem2.get() + memory_size_, memory_size_);
        mem2.swap(mem);
      }
    }
    return mem;
  }

  GzStream get_uncompressing_stream() {
    assert(is_compressed());
    open();
#if ZLIB_VERNUM >= 0x1235
    gzbuffer(file_, 64*1024);
#endif
    return GzStream{file_};
  }

private:
  size_t memory_size_;
  gzFile file_;

  void open() {
    file_ = gzopen(path().c_str(), "rb");
    if (!file_)
      fail("Failed to gzopen: " + path());
  }
};

} // namespace gemmi

#endif
