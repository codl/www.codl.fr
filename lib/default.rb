include Nanoc3::Helpers::Blogging
include Nanoc3::Helpers::Tagging
include Nanoc3::Helpers::LinkTo
include Nanoc3::Helpers::Rendering

def slug str
    str.downcase.gsub(/\s+/, "_")
end

def taglist tags
    tags.map { |tag| "<a href='/tags/#{slug(tag)}'>#{tag}</a>" }.join(", ")
end

def all_tags
  tags = Set.new

  articles.each do |item|
    item[:tags].each { |t| tags.add(t) } if item[:tags]
  end

  tags.sort { |l, r| slug(l) <=> slug(r) }
end
