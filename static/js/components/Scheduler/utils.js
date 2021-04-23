const hexToRGBA = (hex, alpha = 1) => {
  if (!hex) {
    return `rgba(200,200,200,${alpha})`;
  }
  const [r, g, b] = hex.match(/\w\w/g).map((x) => parseInt(x, 16));
  return `rgba(${r},${g},${b},${alpha})`;
};

module.exports = {
  hexToRGBA,
};
