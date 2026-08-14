#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

CANONICAL_FIELDS = %w[name description license compatibility metadata].freeze
NAME_PATTERN = /\A[a-z0-9]+(?:-[a-z0-9]+)*\z/

def fail_check(path, message)
  warn "#{path}: #{message}"
  exit 1
end

skill_directory = ARGV.fetch(0) { abort "usage: skill_packages.rb <skill-directory>" }
skill_path = File.join(skill_directory, "SKILL.md")
begin
  lines = File.readlines(skill_path, encoding: "UTF-8")
  fail_check(skill_path, "missing opening frontmatter delimiter") unless lines.first&.match?(/\A---\s*\z/)

  closing_offset = lines.drop(1).index { |line| line.match?(/\A---\s*\z/) }
  fail_check(skill_path, "missing closing frontmatter delimiter") unless closing_offset

  closing_index = closing_offset + 1
  frontmatter = YAML.safe_load(
    lines[1...closing_index].join,
    permitted_classes: [],
    permitted_symbols: [],
    aliases: false
  )
  fail_check(skill_path, "frontmatter must be a mapping") unless frontmatter.is_a?(Hash)

  unexpected = frontmatter.keys.map(&:to_s) - CANONICAL_FIELDS
  fail_check(skill_path, "unexpected frontmatter field(s): #{unexpected.sort.join(', ')}") unless unexpected.empty?

  name = frontmatter["name"]
  expected_name = File.basename(skill_directory)
  unless name.is_a?(String) && name.length.between?(1, 64) && NAME_PATTERN.match?(name)
    fail_check(skill_path, "name must be 1-64 lowercase kebab-case characters")
  end
  fail_check(skill_path, "name #{name.inspect} does not match directory #{expected_name.inspect}") unless name == expected_name

  description = frontmatter["description"]
  unless description.is_a?(String) && description.length.between?(1, 1024)
    fail_check(skill_path, "description must be 1-1024 characters")
  end

  license = frontmatter["license"]
  fail_check(skill_path, "license must be text when present") if license && !license.is_a?(String)

  compatibility = frontmatter["compatibility"]
  if compatibility && (!compatibility.is_a?(String) || compatibility.length > 500)
    fail_check(skill_path, "compatibility must be text of at most 500 characters")
  end

  metadata = frontmatter["metadata"]
  if metadata && (!metadata.is_a?(Hash) || metadata.any? { |key, value| !key.is_a?(String) || !value.is_a?(String) })
    fail_check(skill_path, "metadata must contain only string keys and values")
  end

  body_lines = lines.length - closing_index - 1
  fail_check(skill_path, "body exceeds 500 lines") if body_lines > 500

  puts "skill-package: #{skill_directory}"
rescue Psych::Exception, ArgumentError, Errno::ENOENT, EncodingError => error
  fail_check(skill_path, error.message)
end
