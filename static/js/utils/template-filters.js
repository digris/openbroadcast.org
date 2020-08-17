
import dayjs from 'dayjs';
import advancedFormat from 'dayjs/plugin/advancedFormat';

dayjs.extend(advancedFormat);

const msToTime = (ms) => {
  if (ms === undefined) {
    return '';
  }

  if (ms === 0) {
    return '00:00';
  }

  let time = Math.abs(ms);

  time = parseInt(time / 1000, 10);
  const seconds = time % 60;
  time = parseInt(time / 60, 10);
  const minutes = time % 60;
  time = parseInt(time / 60, 10);
  const hours = time % 24;
  let out = '';

  if (hours && hours > 0) {
    if (hours < 10) {
      out += '0';
    }
    out += `${hours}:`;
  }

  if (minutes && minutes > 0) {
    if (minutes < 10) {
      out += '0';
    }
    out += `${minutes}:`;
  } else {
    out += '00:';
  }

  if (seconds && seconds > 0) {
    if (seconds < 10) {
      out += '0';
    }
    out += `${seconds}`;
  } else {
    out += '00';
  }

  return out.trim();
};

const sToTime = (s) => msToTime(s * 1000);


export function dayjsFormat(value, format = 'MMM. D, YYYY') {
  const datetime = (typeof value === 'string') ? dayjs(value) : value;
  return datetime.format(format);
}

export const templateFilters = {
  sToTime(value) {
    return sToTime(value);
  },
  msToTime(value) {
    return msToTime(value);
  },
  date(value, format) {
    return dayjsFormat(value, format);
  },
};
