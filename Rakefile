require "rubygems"
require "tmpdir"

require "bundler/setup"
require "jekyll"

# Automate publishing

# Once repo is ready you can render your website and push compiled sources into master branch. But doing it manually is a pain, so let’s add simple rake task. Create (if you don’t have one yet) a Rakefile and add following into it:

############
############


# Change your GitHub reponame
GITHUB_REPONAME = "cc-ai/cc-ai.github.io"

# Enable Google Analytics
ENV["JEKYLL_ENV"] = "production"


desc "Generate blog files"
task :generate do
  Jekyll::Site.new(Jekyll.configuration({
    "source"      => ".",
    "destination" => "_site",
    "JEKYLL_ENV" => "production"
  })).process
end


desc "Generate and publish blog to gh-pages"
task :publish => [:generate] do
  Dir.mktmpdir do |tmp|
    cp_r "_site/.", tmp

    pwd = Dir.pwd
    Dir.chdir tmp

    system "git init"
    system "git add ."
    message = "Site updated at #{Time.now.utc}"
    system "git commit -m #{message.inspect}"
    system "git remote add origin git@github.com:#{GITHUB_REPONAME}.git"
    system "git push origin master --force"

    Dir.chdir pwd
  end
end
