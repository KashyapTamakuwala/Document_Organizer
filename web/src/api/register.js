import axiosInstance from '../config/axiosConfig';

const register = async (payload) => axiosInstance('/user/register', {
  method: 'POST',
  data: payload,
})
  .then((response) => response);

export default register;
