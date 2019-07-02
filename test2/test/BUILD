py_test(
    	name = "testOne",
	srcs = ["testOne.py"],
	deps = [
		"//src:libFunc",
	],
)

py_test(
    	name = "testTwo",
	srcs = ["testTwo.py"],
	deps = [
		"//src:libFunc",
	],
)

test_suite(
    name = "testAll",
    tests = [
        "testOne",
        "testTwo",
    ],
)
