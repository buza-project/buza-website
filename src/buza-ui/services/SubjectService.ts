import { HttpService } from "./HttpService";

export class SubjectService {
  static readonly SUBJECTS_ROUTE = '/subjects';

  static toggleFollowSubject(subjectId: string, following: boolean): Promise<any> {
    if (following) {
    return HttpService.post(`${SubjectService.SUBJECTS_ROUTE}/${subjectId}/unfollow`, {});
    } else {
    return HttpService.post(`${SubjectService.SUBJECTS_ROUTE}/${subjectId}/follow`, {});
    }
  }
}
