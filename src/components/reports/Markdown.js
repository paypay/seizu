import React from 'react';
import PropTypes from 'prop-types';
import Markdoc from '@markdoc/markdoc';
// eslint-disable-next-line  import/no-extraneous-dependencies
import neo4j from 'neo4j-driver';
import { Neo4jContext } from 'use-neo4j';

export default function Markdown({ markdown, markdownSettings, queries }) {
  const { driver, database } = React.useContext(Neo4jContext);
  const [variableData, setVariableData] = React.useState({});

  React.useEffect(() => {
    markdownSettings.variables.forEach((variable) => {
      const session = driver.session({
        database,
        defaultAccessMode: neo4j.session.READ
      });
      const params = {};
      variable.params.forEach((param) => {
        params[param.name] = param.value;
      });
      const query = queries[variable.cypher];
      session
        .run(query, params)
        .then((result) => {
          setVariableData({
            ...variableData,
            [variable.name]: { records: result.records }
          });

          session.close();
        })
        .catch((error) => {
          setVariableData({
            ...variableData,
            [variable.name]: { records: {}, error }
          });
          console.log(error);

          session.close();
        });
    });
  }, [markdown, markdownSettings, queries]);

  const value = {
    transform(parameters) {
      const [variable, key] = Object.values(parameters);

      try {
        const ret = variableData[variable].records[0].get(key);
        if (neo4j.isInt(ret)) {
          return neo4j.int(ret).toNumber();
        }
        return ret;
      } catch (e) {
        return '';
      }
    }
  };

  const config = {
    tags: {},
    nodes: {},
    variables: variableData,
    functions: {
      value
    }
  };
  const ast = Markdoc.parse(markdown);
  const content = Markdoc.transform(ast, config);

  return Markdoc.renderers.react(content, React, {});
}

Markdown.propTypes = {
  markdown: PropTypes.string,
  markdownSettings: PropTypes.object,
  queries: PropTypes.object
};
