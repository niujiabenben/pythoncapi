#include <iostream>
#include <opencv2/core/core.hpp>

#include "ext.h"

cv::Mat ExtCreateCvMat(const char* data, const int rows, const int cols) {
  if (data && rows > 0 && cols > 0) {
    return cv::Mat(rows, cols, CV_8UC3, (void*) data);
  }
  return cv::Mat();
}

extern "C" bool ExtStitchAndSaveImage(const char* top_left_data,
                                      const int top_left_rows,
                                      const int top_left_cols,
                                      const char* top_right_data,
                                      const int top_right_rows,
                                      const int top_right_cols,
                                      const char* bottom_left_data,
                                      const int bottom_left_rows,
                                      const int bottom_left_cols,
                                      const char* bottom_right_data,
                                      const int bottom_right_rows,
                                      const int bottom_right_cols,
                                      const char* save_path) {
  return StitchAndSaveImage(
      ExtCreateCvMat(top_left_data, top_left_rows, top_left_cols),
      ExtCreateCvMat(top_right_data, top_right_rows, top_right_cols),
      ExtCreateCvMat(bottom_left_data, bottom_left_rows, bottom_left_cols),
      ExtCreateCvMat(bottom_right_data, bottom_right_rows, bottom_right_cols),
      save_path);
}
