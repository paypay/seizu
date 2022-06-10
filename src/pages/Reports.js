import { useContext, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import {
  Box,
  Divider,
  Grid,
  Container,
  Paper,
  Typography
} from '@mui/material';
import Loader from 'react-loader-spinner';
import Error from '@mui/icons-material/Error';

import { ConfigContext } from 'src/config.context';
import { getQueryStringValue } from 'src/components/QueryString';
import CypherBar from 'src/components/reports/CypherBar';
import CypherPie from 'src/components/reports/CypherPie';
import CypherProgress from 'src/components/reports/CypherProgress';
import CypherCount from 'src/components/reports/CypherCount';
import CypherTable from 'src/components/reports/CypherTable';
import CypherVerticalTable from 'src/components/reports/CypherVerticalTable';
import CypherAutocomplete from 'src/components/reports/CypherAutocomplete';
import FreeTextInput from 'src/components/reports/FreeTextInput';
import CypherOncallTable from 'src/components/reports/CypherOncallTable';
import OncallTable from 'src/components/reports/OncallTable';
import Markdown from 'src/components/reports/Markdown';

function Reports() {
  const { id } = useParams();
  const { config } = useContext(ConfigContext);
  const { reports, queries } = config.config;
  const report = reports[id];

  const initialVarState = {};
  if (report.inputs) {
    report.inputs.forEach((input) => {
      const inputValue = getQueryStringValue(input.input_id);
      if (inputValue !== undefined) {
        // TODO(ryan-lane): Figure out a way to pass the label along with the value in the param
        initialVarState[input.input_id] = {
          label: inputValue,
          value: inputValue
        };
      } else if (input.default !== undefined) {
        initialVarState[input.input_id] = input.default;
      } else {
        initialVarState[input.input_id] = {};
      }
    });
  }
  const [varData, setVarData] = useState(initialVarState);

  if (config === undefined) {
    return <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />;
  }

  const head = [];
  if (report.inputs) {
    report.inputs.forEach((input) => {
      let inputComponent;

      if (input === undefined) {
        head.push(
          <Grid
            item
            key={input.input_id}
            lg={3}
            md={3}
            xl={3}
            xs={3}
            sx={{ pl: 3, pb: 2, pr: 3 }}
          >
            <Paper elevation={1} sx={{ p: 2 }}>
              <Error />
              <Typography>Undefined input id: {input.input_id}</Typography>
            </Paper>
          </Grid>
        );
        return;
      }

      if (input.type === 'autocomplete') {
        inputComponent = (
          <CypherAutocomplete
            cypher={input.cypher}
            params={input.params}
            inputId={input.input_id}
            inputDefault={input.default}
            labelName={input.label}
            value={varData}
            setValue={setVarData}
          />
        );
      } else if (input.type === 'text') {
        inputComponent = (
          <FreeTextInput
            inputId={input.input_id}
            inputDefault={input.default}
            labelName={input.label}
            value={varData}
            setValue={setVarData}
          />
        );
      }
      let size;
      let xsSize;
      if (input.size === undefined) {
        size = 3;
        xsSize = 6;
      } else if (input.size < 7) {
        xsSize = input.size * 2;
      } else {
        xsSize = input.size;
      }
      head.push(
        <Grid
          item
          key={input.input_id}
          lg={size}
          md={size}
          xl={size}
          xs={xsSize}
          sx={{ pl: 3, pb: 2, pr: 3 }}
        >
          <Paper elevation={1} sx={{ p: 2 }}>
            {inputComponent}
          </Paper>
        </Grid>
      );
    });
  }

  const rows = [];
  report.rows.forEach((row) => {
    const items = [];
    row.panels.forEach((item, index) => {
      const needInputs = [];
      const params = {};
      if (item.params !== undefined) {
        item.params.forEach((inputData) => {
          const paramName = inputData.name;
          const paramValue = inputData?.value;
          const paramInputId = inputData?.input_id;
          if (paramValue !== null) {
            params[paramName] = paramValue;
          } else if (paramInputId !== null) {
            params[paramName] = varData[paramInputId]?.value;
            if (
              params[paramName] === undefined ||
              params[paramName] === null ||
              params[paramName] === ''
            ) {
              try {
                const input = report.inputs.find(
                  (obj) => obj.input_id === paramInputId
                );
                needInputs.push(input.label);
              } catch (error) {
                console.log(error);
                needInputs.push(`*(Error: undefined input: ${paramInputId})`);
              }
            }
          }
        });
      }

      const details = {
        cypher: queries[item.cypher],
        details_cypher: queries[item.details_cypher],
        type: item.type,
        metric: item.metric,
        columns: item.columns,
        caption: item.caption,
        params
      };

      let itemComponent;
      if (item.type === 'progress') {
        itemComponent = (
          <CypherProgress
            cypher={queries[item.cypher]}
            params={params}
            caption={item.caption}
            threshold={item.threshold}
            details={details}
            needInputs={needInputs}
          />
        );
      } else if (item.type === 'pie') {
        itemComponent = (
          <CypherPie
            cypher={queries[item.cypher]}
            params={params}
            caption={item.caption}
            pieSettings={item.pie_settings}
            details={details}
            legend={item.legend}
          />
        );
      } else if (item.type === 'bar') {
        itemComponent = (
          <CypherBar
            cypher={queries[item.cypher]}
            params={params}
            caption={item.caption}
            barSettings={item.bar_settings}
            details={details}
            legend={item.legend}
          />
        );
      } else if (item.type === 'count') {
        itemComponent = (
          <CypherCount
            cypher={queries[item.cypher]}
            params={params}
            caption={item.caption}
            details={details}
            needInputs={needInputs}
          />
        );
      } else if (item.type === 'table') {
        itemComponent = (
          <CypherTable
            cypher={queries[item.cypher]}
            params={params}
            columns={item.columns}
            caption={item.caption}
            details={details}
            needInputs={needInputs}
          />
        );
      } else if (item.type === 'vertical-table') {
        itemComponent = (
          <CypherVerticalTable
            cypher={queries[item.cypher]}
            params={params}
            id={item.table_id}
            details={details}
            needInputs={needInputs}
          />
        );
      } else if (item.type === 'oncall-table') {
        if (item.cypher === undefined) {
          itemComponent = (
            <OncallTable
              caption={item.caption}
              enabled={config.pagerduty_enabled}
            />
          );
        } else {
          itemComponent = (
            <CypherOncallTable
              cypher={queries[item.cypher]}
              params={params}
              caption={item.caption}
              needInputs={needInputs}
              enabled={config.pagerduty_enabled}
            />
          );
        }
      } else if (item.type === 'markdown') {
        itemComponent = (
          <Markdown
            markdown={item.markdown}
            markdownSettings={item.markdown_settings}
            queries={queries}
          />
        );
      }
      let size;
      let xsSize;
      if (item.size === undefined) {
        size = 3;
        xsSize = 6;
      } else if (item.size < 7) {
        xsSize = item.size * 2;
      } else {
        xsSize = item.size;
      }
      items.push(
        // We allow index in keys here because the config isn't reloaded, and as such elements
        // in the config will never change.
        // eslint-disable-next-line react/no-array-index-key
        <Grid item key={index} lg={size} md={size} xl={size} xs={xsSize}>
          {itemComponent}
        </Grid>
      );
    });
    rows.push(
      <Container key={row.name} maxWidth={false} sx={{ pb: 2 }}>
        <Paper elevation={1} sx={{ p: 2 }}>
          <Typography gutterBottom variant="h2">
            {row.name}
          </Typography>
          <Divider />
          <Grid container spacing={2} sx={{ py: 2 }}>
            {items}
          </Grid>
        </Paper>
      </Container>
    );
  });

  return (
    <>
      <Helmet>
        <title>{report.name} | Seizu</title>
      </Helmet>
      <Box
        sx={{
          height: '100%',
          py: 3
        }}
      >
        <Grid container>
          {head}
          {rows}
        </Grid>
      </Box>
    </>
  );
}

export default Reports;
