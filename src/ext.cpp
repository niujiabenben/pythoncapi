#include "ext.h"

void ResizeKeepRatio(const cv::Mat& src, const cv::Mat& dst) {
  if (src.empty()) { return; }
  if ((src.rows <= dst.rows) && (src.cols <= dst.cols)) {
    int x = (dst.cols - src.cols) / 2;
    int y = (dst.rows - src.rows) / 2;
    src.copyTo(dst(cv::Rect(x, y, src.cols, src.rows)));
  } else {
    int new_rows = dst.rows;
    int new_cols = new_rows * src.cols / src.rows;
    if (new_cols > dst.cols) {
      new_cols = dst.cols;
      new_rows = new_cols * src.rows / src.cols;
    }
    int x = (dst.cols - new_cols) / 2;
    int y = (dst.rows - new_rows) / 2;
    cv::Rect roi(x, y, new_cols, new_rows);
    cv::resize(src, dst(roi), cv::Size(new_cols, new_rows));
  }
}

bool StitchAndSaveImage(const cv::Mat& top_left,
                        const cv::Mat& top_right,
                        const cv::Mat& bottom_left,
                        const cv::Mat& bottom_right,
                        const std::string& save_path) {
  const int width = 512;
  const int height = 384;
  const cv::Scalar background(0, 0, 0);
  cv::Mat sticthed(height * 2, width * 2, CV_8UC3, background);

  cv::Rect top_left_roi(0, 0, width, height);
  cv::Rect top_right_roi(width, 0, width, height);
  cv::Rect bottom_left_roi(0, height, width, height);
  cv::Rect bottom_right_roi(width, height, width, height);
  ResizeKeepRatio(top_left, sticthed(top_left_roi));
  ResizeKeepRatio(top_right, sticthed(top_right_roi));
  ResizeKeepRatio(bottom_left, sticthed(bottom_left_roi));
  ResizeKeepRatio(bottom_right, sticthed(bottom_right_roi));

  auto dirname = boost::filesystem::path(save_path).parent_path();
  if (!boost::filesystem::exists(dirname)) {
    boost::filesystem::create_directories(dirname);
  }
  return cv::imwrite(save_path, sticthed);
}
