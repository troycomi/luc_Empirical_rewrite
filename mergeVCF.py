from optparse import OptionParser
import sys


# class for returning parsed lines.
class VcfLine():
    def __init__(self,
                 chromosome=0,
                 position=0,
                 ref="",
                 alt="",
                 genotype=[]):
        self.chromosome = chromosome
        self.position = position
        self.ref = ref
        self.alt = alt
        self.genotype = genotype


def main():
    parser = buildParser()
    (options, args) = parser.parse_args()
    validateOptions(options)

    with open(options.inputArchaic, "r") as inputvcf:
        with open(options.output, "w") as output:

            # this has to be read with readline instead of for loop
            # to handle case where current line needs to be re-examined
            vcfLine = inputvcf.readline()

            for stdLine in sys.stdin:
                std = breakVcfLine(stdLine, '#')
                if std is None:
                    continue

                while vcfLine != "":
                    vcf = breakVcfLine(vcfLine, '#')
                    # in contrast to stdin, here we don't
                    # care about line with 2 chars
                    if vcf is None or vcf.ref is None:
                        vcfLine = inputvcf.readline()
                        continue

                    if vcf.position < std.position:
                        if any([gen == 1 or gen == 2
                                for gen in vcf.genotype]):

                            output.write("\t".join(str(x) for x in
                                                   [vcf.chromosome,
                                                   vcf.position,
                                                   vcf.ref,
                                                   vcf.alt]))
                            output.write("\t")
                            output.write("\t".join(str(x)
                                                   for x in vcf.genotype))
                            output.write("\t")
                            output.write("\t".join(["0"]*len(std.genotype)))
                            output.write("\t\n")  # to match c++ code
                        vcfLine = inputvcf.readline()

                    elif vcf.position == std.position:
                        if vcf.ref == std.ref and \
                                (vcf.alt == '.' or
                                 vcf.alt == std.alt):
                            output.write("\t".join(str(x) for x in
                                                   [vcf.chromosome,
                                                   vcf.position,
                                                   vcf.ref,
                                                   std.alt]))
                            output.write("\t")
                            output.write("\t".join(str(x)
                                                   for x in vcf.genotype))
                            output.write("\t")
                            output.write("\t".join(str(x)
                                                   for x in std.genotype))
                            output.write("\t\n")
                            vcfLine = inputvcf.readline()
                            break
                        vcfLine = inputvcf.readline()

                    else:  # greater than, have to look at this line again
                        break


def buildParser():
    """Builds a simple parser for input vcf and output txt file"""

    usage = "usage: python mergeVCF.py -a ARCHAIC_VCF \
        -o OUTPUT_FILE <TABIX_OUTPUT"
    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--archaic",
                      type="string",
                      dest="inputArchaic",
                      help="input archaic vcf file; required")

    parser.add_option("-o", "--output",
                      type="string",
                      dest="output",
                      help="output text file name; required")

    return parser


def validateOptions(options):
    """Checks that all required arguments are provided.
        Raises ValueError when a required value is not
        defined.
    """

    if not options.inputArchaic:
        raise ValueError("Archaic vcf filename not provided")

    if not options.output:
        raise ValueError("Output filename not provided")


def breakVcfLine(line, char):
    """Splits a vcf line to components as VCF line object
        Any lines starting with 'char' are returned as None"""
    if line[0] == char:
        return None

    tokens = line.split('\t')

    result = VcfLine(
        chromosome=int(tokens[0]),
        position=int(tokens[1]),
        ref=tokens[3],
        alt=tokens[4],
        genotype=[]
    )

    # there is an odd case where we need to skip this
    # when stdin has to chars but vcf does not
    if len(result.ref) > 1 or len(result.alt) > 1:
        result.ref = None

    # for all columns from 9 over
    for lineInfo in tokens[9:]:
        if result.ref is None:
            result.genotype.append(0)
        else:
            # convert lines like 0|1 and 1/1 to 0 and 1 respectively
            if(lineInfo[1] == '/' or lineInfo[1] == '|'):
                result.genotype.append(int(lineInfo[0]) + int(lineInfo[2]))
            else:
                result.genotype.append(9)  # flag used in c++ code

    return result


def discardToChar(stream, char):
    """Read from the given stream until first char in line is no longer char
        First line without char is at top of file
        Returns first line without char"""
    line_pos = stream.tell()
    line = stream.readline()
    while line != "":
        if line[0] != char:
            stream.seek(line_pos)
            return line
        line_pos = stream.tell()
        line = stream.readline()


if __name__ == "__main__":
    main()
