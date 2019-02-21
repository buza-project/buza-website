import React from 'react';
import { truncateText } from '../../utils/StringUtils';
import { SubjectService } from '../../services/SubjectService';

const AnonymousSubjectCard = ({ subject }) => (
  <div className="card mb-1 subject__card_follow ">
    <a
      href={`${SubjectService.SUBJECTS_ROUTE}/${subject.pk}`}
      className="subject__title_follow"
    >
      {truncateText(subject.title, 23)}
    </a>
  </div>
);

export default AnonymousSubjectCard;
