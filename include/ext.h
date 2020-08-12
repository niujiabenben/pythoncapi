#ifndef PYTHONCAPI_EXT_H_
#define PYTHONCAPI_EXT_H_

#include <boost/filesystem.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <vector>

bool StitchAndSaveImage(const cv::Mat& top_left,
                        const cv::Mat& top_right,
                        const cv::Mat& bottom_left,
                        const cv::Mat& bottom_right,
                        const std::string& save_path);

#endif  // PYTHONCAPI_EXT_H_
