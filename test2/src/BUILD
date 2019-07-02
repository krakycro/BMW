py_library(
	name = "libFunc",
	srcs = ["libFunc.py"],
	visibility = ["//visibility:public"],
)

py_binary(
	name = "mainFunc",
	srcs = ["mainFunc.py"],
	deps = [
		"libFunc",
	],
	visibility = ["//visibility:public"],
)
