export default function oneProblemSection(output) {
  const headings = output.match(/^[ \t]*(?:#{1,6} +Problem[:# ]*$|\*\*Problem[.:]?\*\*[.:]?(?=[ \t]|$))/gim);
  return headings?.length === 1;
}
