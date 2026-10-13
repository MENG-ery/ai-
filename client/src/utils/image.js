// 图片地址处理：海信 / 海尔官方商城图片有防盗链，改写为开发服务器代理地址
const HOST_MAP = [
  [/^https?:\/\/img\.shop\.hisense\.com/, '/hisense-img'],
  [/^https?:\/\/image\.haier\.com/, '/haier-img'],
];

export function resolveImage(url) {
  if (!url) return '';
  let out = url;
  for (const [pattern, replacement] of HOST_MAP) {
    out = out.replace(pattern, replacement);
  }
  return out;
}
