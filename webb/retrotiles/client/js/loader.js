export async function loadSprites(src) {
  const res = await fetch(src)
  const blob = await res.blob()
  return(await createImageBitmap(blob))
}

