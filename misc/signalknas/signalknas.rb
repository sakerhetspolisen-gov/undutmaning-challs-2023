#!/usr/bin/env ruby
#
require 'base64'
require 'tmpdir'
require 'English'
require 'optparse'

# Check if command is in PATH.
#
# @param [String] cmd command.
# @return [Boolean] true if command is present, otherwise false.
def command?(cmd)
  `which #{cmd}`
  $CHILD_STATUS.success?
end


@probs = {
  deletion: 0.1,
  insertion: 0.1,
  mutation: 0.15
}


@keys = ["00", "01", "10", "11"]
@vals = [8216, 8217, 8220, 8221].map{|c| c.chr 'utf-8'}
@map = Hash[@keys.zip(@vals.shuffle)]

def encode(char)
  dibits = ("%08b" % char.ord).scan(/.{2}/)
  dibits.collect{|b| @map[b]}
end

def addnoise(distr)
  res = []
  i = 0
  while(i < distr.size) do
    c = distr[i]
    r = rand
    #p r
      case r
      when 0..@probs[:deletion]
        i += 1
        #p "del"
        next
      when @probs[:deletion]..@probs[:insertion]
        res.push(@vals.sample)
        res.push(c)
        #p "ins" + res[-1]
        next
      when @probs[:insertion]..@probs[:mutation] 
        res.push((@vals - [c]).sample)
        #p "mut "
        i += 1
        next
      else
        res.push(c)
        i += 1
      end
    end

  return(res.join(""))
end

def generate(seq)
  sample = ""
  seq.each do |c|
    sample << addnoise(c)
  end

  return(sample)
end

def reconstruct_sequence(c, verbose= false, trueseq = nil)
  map = Hash[@map.values.zip(['C', 'G', 'A', 'T'])]
  Dir.mktmpdir do |dir|
    fname = dir + "/seq.txt"
    f = File.open(fname, "w")
    f.write("CLUSTALW\n\n")
    c.each_with_index do |s, i|
      seq = s.split("").collect{|s| map[s]}.join("")
      f.write("%02d %s\n" % [i, seq])
    end
    f.write("\n")
    f.close

    `cd #{dir} && clustalw -align -output=GCG -type=DNA -infile=#{fname}`
    `cd #{dir} && em_cons -sequence seq.msf -outseq aligned.txt 2>/dev/null`
    @seq = `grep -v EMBOSS #{dir + "/aligned.txt"}`.gsub("\n","")
    @seq.gsub!("n","")
  end
  if(trueseq)
    revmap = Hash[@map.values.zip(['C', 'G', 'A', 'T'])]
    ans = trueseq.split("").collect{|c| revmap[c]}.join("")
    if( @seq != ans)
      if(verbose)
        STDERR.print("Orig: #{ans}\n")
        STDERR.print("Recs: #{@seq}\n")
      end
      raise "mismatch!"
    else
      STDERR.print("Successful reconstruction.\n")
    end
  end
  return(@seq)
end

def solve(seq)
  res = []
  symbols = seq.split("").uniq
  chars = seq.scan(/.{4}/)
  @keys.permutation.each do |k|
    map = Hash[symbols.zip(k)]
    str = []
    chars.each do |p|
      str << p.split("").collect{|x| map[x]}.join("").to_i(2)
    end
    if str.all?{|x| x > 31 && x < 127}
      res.push(str.map{|x| x.chr}.join("").force_encoding('ISO8859-1').encode('utf-8'))
    end
  end
  return(res)
end

def main()
  opts = {}
  options_parser = OptionParser.new do |parser|
    parser.on("-h", "--help", "print this help") do
      puts parser
      exit
    end
    parser.on('-s', '--solve', "solve challenge") do |d|
      opts[:solve] = true
    end
    parser.on('-v', '--verbose', "verbose output") do |d|
      opts[:verbose] = true
    end
  end
  options_parser.banner = "signalknas.rb - create or solve signalknas challenge."
  options_parser.separator "Create: signalknas.rb N FLAGSTRING"
  options_parser.separator "Solve: cat input.txt | signalknas.rb -s\n\n"
  options_parser.parse!
  @n = ARGV[0].to_i
  @str = ARGV[1]

  # check that required software is installed
  if(!command?("clustalw") || !command?("em_cons"))
    print("Error: clustalw and em_cons required.\n")
    print("to install: apt install clustalw emboss\n")
    exit
  end
  if(opts[:solve])
    cipher = ARGF.read
    seq = reconstruct_sequence(cipher.split("\n"), opts[:verbose])
    print("Possible solutions:\n\n")
    print solve(seq).join("\n")
    exit
  else
    seq = @str.split("").collect{|c| encode(c)}
    STDERR.print "Correct message string:\n"
    STDERR.print seq.join("") + "\n\n"
    1000.times do
      begin
        cipher = []
        @n.times do
          cipher.push(generate(seq))
        end
        seq = reconstruct_sequence(cipher, opts[:verbose], @str.split("").collect{|c| encode(c)}.join(""))
        print cipher.join("\n") + "\n"
        STDERR.puts solve(seq)
        exit
      rescue
        next
      end
    end
    STDERR.print "Error: did manage to create a solvable challenge.\n"
  end
end

main
