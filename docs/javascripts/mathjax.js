// MathJax configuration for pymdownx.arithmatex in generic mode.
//
// Every section's "Do the Math" block is LaTeX, so this is load-bearing rather
// than decorative: without it the formulas render as literal $$...$$ text and
// the markdown parser turns underscores inside \text{} into emphasis tags.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// Re-typeset after Material's instant-loading navigation swaps the page body.
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
