import axios from 'axios';

export class HttpService {
  static post(url: string, body: any): Promise<any> {
    return axios.post(url, body);
  }
}