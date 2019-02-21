import * as React from 'react';
import * as ReactDOM from 'react-dom';

import SubjectCard from '../components/subjectCards/SubjectCard';

interface Props {
  subjects: any[];
  userSubjects: any[];
  selectedSubjectId: string;
}

const SubjectCards = ({ subjects, userSubjects, selectedSubjectId }: Props) => (
  <div className="subject__deck">
    {subjects.map((subject, index) => (
      <SubjectCard
        key={index}
        subject={subject}
        selected={subject.pk === selectedSubjectId}
        following={userSubjects.indexOf(subject) > -1}
      />
    ))}
  </div>
);

SubjectCards.defaultProps = {
  userSubjects: []
};

if ((window as any).reactEntrypoint) {
  ReactDOM.render(
    <SubjectCards {...(window as any).props} />,
    (window as any).reactEntrypoint
  );
}
