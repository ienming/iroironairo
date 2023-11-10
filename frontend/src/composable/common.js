export function hsl2Hex(h, s, l) {
    l /= 100;
    const a = s * Math.min(l, 1 - l) / 100;
    const f = n => {
      const k = (n + h / 30) % 12;
      const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
      return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
    };
    let result = `#${f(0)}${f(8)}${f(4)}`
    return result.toUpperCase();
  }

export function hex2Rgb(hex) {
  // 移除Hex顏色值中的#字符（如果存在）
  hex = hex.replace(/^#/, '');

  // 將Hex值拆分成RR、GG和BB部分
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);

  // 返回RGB數值作為對象
  return { r, g, b };
}

export function getReverseColor(hslObj){
  if (25 < hslObj.l && hslObj.l < 75) {
    return {
      'h': 360,
      's': 0,
      'l': 100,
    }
  } else {
    return {
      'h': hslObj.h,
      's': hslObj.s,
      'l': 100 - hslObj.l,
    }
  }
}