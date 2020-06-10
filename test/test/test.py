#!/usr/bin/env python3
from subprocess import Popen, PIPE, TimeoutExpired
import filecmp
import subprocess
import re


def comp(name):
    return True
    # p = Popen("javac " + name, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # output, err = p.communicate(b"")
    # rc = p.returncode
    # return (rc == 0)


def test_example(c):
    name = c[0]
    point = float(c[1])
    case = c[2:]
    ans = open(name)
    answer = open(name).read()

    name = name.split('/')[1]
    # print("answer:\n ", answer)

    try:
        ans = [line.lower() for line in ans]
        ans = list(filter(lambda x: not re.match(r'^\s*$', x), ans))
        for i in range(len(ans)):
            while ans[i][-1] == '\n' or ans[i][-1] == ' ' or ans[i][-1] == '\r':
                ans[i] = ans[i][:-1]
                

        # get the student output
        case[2] = ' '.join(case[2:])
        # print('Case:', case[:3])
        p = subprocess.run(case[:3], stdin=PIPE, stdout=PIPE, stderr=PIPE, timeout=100)
        output = p.stdout.decode("utf-8")

        # output = "".join(output.split())
        # answer = "".join(answer.split())

        # output = output.rstrip()
        # answer = answer.rstrip()

        file = open(name, "w+")
        file.write("Output:\n")
        file.write(output)
        file.write("\nSolution:\n")
        file.write(answer)
        file.close()


        output = [line.lower() for line in output.split('\n')]

        out = list(filter(lambda x: not re.match(r'^\s*$', x), output))
        for line in out:
            while line[-1] == '\n' or line[-1] == ' ' or line[-1] == '\r':
                line = line[:-1]

        if (name == 'displayimage.txt') or (name == 'displayimage2.txt') or (name == 'displayimage3.txt') or (name == 'displayimage4.txt') or (name == 'displayimage5.txt') or (name == 'displayimage_formattedplot.txt') or (name == 'submittedorigandproj.txt') or (name == 'submitteddifferwriteup.txt'):
            print("%s: test case passed: " % name, end = '')
            print("%.0f points" % point)
            return point, True
        # print(out)
        if (len(out) == 0):
            print("%s: output nothing " % name)
            return 0, False

        ans.sort()
        out.sort()

        # print("ans: ", ans)
        # print("out: ", out)

        if ans == out:
            print("%s: test case passed: " % name, end = '')
            print("%.0f points" % point)
            return point, True
        else:
            print("%s: output mismatch " % name)
            # print("Answer: ", ans)
            # print("Output: ", out)
            return 0, False
    except TimeoutExpired:
        print("%s: timeout " % name)
        return 0, False
    except:
        print("%s: exception thrown " % name)
        return 0, False


if __name__ == "__main__":
    total = 0
    print("Test P5")

    cases = open("testcases")
    cases = [x.split() for x in cases]
    scores = 0
    for c in cases:
        score, cur = test_example(c)
        scores += score

    total += scores
    print("Scores: %.0f" % total)
