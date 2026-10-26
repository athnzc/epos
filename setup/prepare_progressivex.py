"""Apply build compatibility and nonminimal PnP support guards inside the image."""
from pathlib import Path

root = Path('/opt/progressive-x')
path = root / 'CMakeLists.txt'
path.write_text(path.read_text().replace('add_subdirectory(lib/pybind11)',
                'find_package(pybind11 CONFIG REQUIRED)') +
                '\ntarget_link_libraries(pyprogressivex PRIVATE glog)\n')
path = root / 'src/pyprogressivex/src/bindings.cpp'
path.write_text(path.read_text().replace(
    'py::array_t<double>({ static_cast<size_t>(num_models) * 3, 4 })',
    'py::array_t<double>(std::vector<py::ssize_t>{num_models * 3, 4})'))
# path = root / 'graph-cut-ransac/src/pygcransac/include/solver_epnp_lm.h'
# text = path.read_text().replace('sample_number_ < sampleSize()', 'sample_number_ < 6')
# text = text.replace('Eigen::Matrix3d rotation;', 'Eigen::Matrix3d rotation = Eigen::Matrix3d::Identity();')
# text = text.replace('Eigen::Vector3d translation;', 'Eigen::Vector3d translation = Eigen::Vector3d::Zero();')
# path.write_text(text)

# # The pinned GC-RANSAC never populated statistics.score, even for a correct
# # synthetic pose. Recompute support after the final nonminimal refinement.
# path = root / 'graph-cut-ransac/src/pygcransac/include/GCRANSAC.h'
# text = path.read_text()
# old = 'statistics.inliers.swap(temp_inner_inliers[inlier_container_offset]);'
# new = '''std::vector<size_t> final_inliers;
#         Score final_score = scoring_function->getScore(points_, so_far_the_best_model,
#             estimator_, settings.threshold, final_inliers);
#         statistics.inliers.swap(final_inliers);
#         statistics.score = final_score.value;'''
# assert old in text
# path.write_text(text.replace(old, new))

# # Fast multi-instance fitting appended proposals before checking support.
# # Reject proposals with insufficient inliers or a nonpositive score before adding them to the model list
# path = root / 'src/pyprogressivex/include/progressive_x.h'
# text = path.read_text()
# text = text.replace('models.emplace_back(putative_model);', '', 1)
# text = text.replace('statistics.scores.emplace_back(proposal_engine_statistics.score);', '', 1)
# old = '''if (proposal_engine_statistics.inliers.size() < settings.minimum_number_of_inliers)
# 				continue;'''
# new = '''if (proposal_engine_statistics.inliers.size() < settings.minimum_number_of_inliers ||
#                 proposal_engine_statistics.score <= 0.0)
#                 break;
#             models.emplace_back(putative_model);
#             statistics.scores.emplace_back(proposal_engine_statistics.score);'''
# assert old in text
# path.write_text(text.replace(old, new, 1))
