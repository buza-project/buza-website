
export const truncateText = (text: string, length: number = 50, end: string = '...'): string =>
 !!text ? text.substring(0, length) + end : '';