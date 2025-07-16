import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Easy to Use',
    description: (
      <>
        Evalap was designed from the ground up to be easily installed and
        used to get your evaluation experiments up and running quickly.
      </>
    ),
  },
  {
    title: 'Focus on What Matters',
    description: (
      <>
        Evalap lets you focus on your models and datasets, and takes care of the
        evaluation infrastructure. Go ahead and evaluate your LLMs.
      </>
    ),
  },
  {
    title: 'Comprehensive Metrics',
    description: (
      <>
        Evaluate your models with a wide range of metrics and easily extend
        with your own custom metrics for specialized evaluation needs.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}