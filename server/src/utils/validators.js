const isValidUrl = (url) => {
  try {
    const normalizedUrl =
      url.startsWith("http://") || url.startsWith("https://")
        ? url
        : `http://${url}`;

    new URL(normalizedUrl);
    return true;
  } catch (error) {
    return false;
  }
};

module.exports = { isValidUrl };