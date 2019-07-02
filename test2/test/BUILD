py_test(
    	name = "testSmokeOne",
	srcs = ["testSmokeOne.py"],
	deps = [
		"//src:libFunc",
	],
	tags = ["smoke"],
)

py_test(
    	name = "testSmokeTwo",
	srcs = ["testSmokeTwo.py"],
	deps = [
		"//src:libFunc",
	],
	tags = ["smoke"],
)

py_test(
    	name = "testFaultOne",
	srcs = ["testFaultOne.py"],
	deps = [
		"//src:libFunc",
	],
	tags = ["fault"],
)

test_suite(
	name = "testSmoke",
	tags = ["smoke"],
)

test_suite(
	name = "testFault",
	tags = ["fault"],
)

test_suite(
	name = "testAll",
)
