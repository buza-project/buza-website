import * as React from 'react';

import { truncateText } from '../../utils/StringUtils';
import { SubjectService } from '../../services/SubjectService';

interface Props {
  subject: any;
  selected: boolean;
  following: boolean;
}

// TODO: Ntokozo: protect this with a anti-csrf token ref https://docs.djangoproject.com/en/2.1/ref/csrf/
const toggleFollowSubject = (subjectId: string, following: boolean): Promise<void> =>
  SubjectService.toggleFollowSubject(subjectId, following);

const buttonClass = (following: boolean) =>
  following
    ? 'subject__buttons subject__buttons-following'
    : 'btn btn-primary subject__buttons subject__buttons-follow';

const SubjectCard = ({ subject, selected, following }: Props) => (
  <div className={`card mb-1 subject__card_following ${selected && 'subject__card_focus'}`}>
    <a href="" className={selected ? 'subject__title_focus' : 'subject__title_following'}>
      <form action="" method="post" className="d-inline-block ">
        <button
          onClick={() => toggleFollowSubject(subject.pk, following)}
          type="submit"
          value={subject.pk}
          name="following-subject"
          className={buttonClass(following)}
        >
          &#9733;
        </button>
      </form>
      {truncateText(subject.title, 23)}
    </a>
  </div>
);

export default SubjectCard;
