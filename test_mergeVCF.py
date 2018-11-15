import pytest
import mergeVCF


def test_parser():
    parser = mergeVCF.buildParser()
    (options, args) = parser.parse_args(
        ["-a", "input.vcf", "-o", "output.txt"])

    try:
        mergeVCF.validateOptions(options)
    except ValueError:
        pytest.fail("Unexpected ValueError")

    assert options.inputArchaic == "input.vcf"
    assert options.output == "output.txt"

    (options, args) = parser.parse_args([])
    with pytest.raises(ValueError):
        mergeVCF.validateOptions(options)

    (options, args) = parser.parse_args(["-a", "input.vcf"])
    with pytest.raises(ValueError):
        mergeVCF.validateOptions(options)

    (options, args) = parser.parse_args(["-o", "output.txt"])
    with pytest.raises(ValueError):
        mergeVCF.validateOptions(options)


def test_breakVcfLine():
    input1 = "1\t9995\t.\tN\tT\t36\t.\t.\tGT:DP:A:C:G:T:PP:GQ\t1/1:2:0,0:0,0:0,0:0,2:63,38,50,0,84,90,48,82,43,48:38"

    output1 = mergeVCF.breakVcfLine(input1)
    assert output1.chromosome == 1
    assert output1.position == 9995
    assert output1.ref == 'N'
    assert output1.alt == 'T'
    assert output1.genotype == [2]

    input2 = "1\t9996\t.\tN\tT\t52\t.\t.\tGT:DP:A:C:G:T:PP:GQ\t1/0:6:0,0:0,0:0,0:0,6:177,131,148,0,185,193,60,178,54,60:54"
    output2 = mergeVCF.breakVcfLine(input2)
    assert output2.chromosome == 1
    assert output2.position == 9996
    assert output2.ref == 'N'
    assert output2.alt == 'T'
    assert output2.genotype == [1]

    # line with too many poly chars
    input3 = "1\t9996\t.\tNA\tT\t52\t.\t.\tGT:DP:A:C:G:T:PP:GQ\t1/0:6:0,0:0,0:0,0:0,6:177,131,148,0,185,193,60,178,54,60:54"
    assert mergeVCF.breakVcfLine(input3) is None

    # line with bad lineInfo
    input4 = "1\t9996\t.\tN\tT\t52\t.\t.\tGT:DP:A:C:G:T:PP:GQ\t1:0:6:0,0:0,0:0,0:0,6:177,131,148,0,185,193,60,178,54,60:54"
    output4 = mergeVCF.breakVcfLine(input4)
    assert output4.chromosome == 1
    assert output4.position == 9996
    assert output4.ref == 'N'
    assert output4.alt == 'T'
    assert output4.genotype == [9]

    input5 = "1\t89567\trs545434463\tG\tA\t100\tPASS\tAC=2\tGT\t0|0\t0|0\t0|0\t0|0\t0|0\t0|0\t0|0"
    output5 = mergeVCF.breakVcfLine(input5)
    assert output5.chromosome == 1
    assert output5.position == 89567
    assert output5.ref == 'G'
    assert output5.alt == 'A'
    assert output5.genotype == [0, 0, 0, 0, 0, 0, 0]
