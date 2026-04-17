const objectKeyToAPIUrl = (key) => {
  // example: alibrary.release:87a71f94-8f2b-4629-801c-b14bdde06838
  const ct = key.split(':')[0];
  const uuid = key.split(':')[1];
  return `/api/v2/${ct.replace('.', '/')}/${uuid}/`;
};

export { objectKeyToAPIUrl };
