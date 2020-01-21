
import dayjs from 'dayjs';
import advancedFormat from 'dayjs/plugin/advancedFormat';

dayjs.extend(advancedFormat);

const _ms_to_time = function (ms) {
  if (ms === undefined) {
    return '';
  }

  if (ms === 0) {
    return '00:00';
  }

  let time = Math.abs(ms);

  const millis = time % 1000;
  time = parseInt(time / 1000);
  const seconds = time % 60;
  time = parseInt(time / 60);
  const minutes = time % 60;
  time = parseInt(time / 60);
  const hours = time % 24;
  let out = '';

  if (hours && hours > 0) {
    if (hours < 10) {
      out += '0';
    }
    out += `${hours}:`;
  } else {
    // out += '0' + ':';
  }

  if (minutes && minutes > 0) {
    if (minutes < 10) {
      out += '0';
    }
    out += `${minutes}:`;
  } else {
    out += '00' + ':';
  }

  if (seconds && seconds > 0) {
    if (seconds < 10) {
      out += '0';
    }
    out += `${seconds}`;
  } else {
    out += '00' + '';
  }

  return out.trim();
};


export function s_to_time(s) {
  return _ms_to_time(s * 1000);
}

export function ms_to_time(ms) {
  return _ms_to_time(ms);
}

export function dayjsFormat(value, format) {
  const datetime = (typeof value === 'string') ? dayjs(value) : value;
  return datetime.format(format);
}

export const templateFilters = {
  s_to_time(value) {
    return s_to_time(value);
  },
  ms_to_time(value) {
    return ms_to_time(value);
  },
  date(value, format) {
    return dayjsFormat(value, format);
  },
};
