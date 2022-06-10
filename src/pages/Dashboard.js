import { useContext } from 'react';
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

import { ConfigContext } from 'src/config.context';
import CypherBar from 'src/components/reports/CypherBar';
import CypherPie from 'src/components/reports/CypherPie';
import CypherProgress from 'src/components/reports/CypherProgress';
import CypherCount from 'src/components/reports/CypherCount';
import CypherTable from 'src/components/reports/CypherTable';
import CypherVerticalTable from 'src/components/reports/CypherVerticalTable';
import OncallTable from 'src/components/reports/OncallTable';
import Markdown from 'src/components/reports/Markdown';

function Dashboard() {
  const { config } = useContext(ConfigContext);

  if (config === undefined) {
    return <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />;
  }
  const { dashboard, queries } = config.config;

  const rows = [];
  dashboard.rows.forEach((row) => {
    const items = [];
    row.panels.forEach((item, index) => {
      const params = {};
      if (item.params !== undefined) {
        item.params.forEach((inputData) => {
          const paramName = inputData.name;
          const paramValue = inputData?.value;
          if (paramValue !== undefined) {
            params[paramName] = paramValue;
          }
        });
      }

      const details = {
        cypher: queries[item.cypher],
        details_cypher: queries[item.details_cypher],
        type: item.type,
        metric: item.metric,
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
          />
        );
      } else if (item.type === 'table') {
        itemComponent = (
          <CypherTable
            cypher={queries[item.cypher]}
            params={params}
            caption={item.caption}
            details={details}
          />
        );
      } else if (item.type === 'vertical-table') {
        itemComponent = (
          <CypherVerticalTable
            cypher={queries[item.cypher]}
            params={params}
            id={item.table_id}
            details={details}
          />
        );
      } else if (item.type === 'oncall-table') {
        itemComponent = (
          <OncallTable
            params={params}
            caption={item.caption}
            enabled={config.pagerduty_enabled}
          />
        );
      } else if (item.type === 'markdown') {
        itemComponent = (
          <Markdown
            markdown={item.markdown}
            markdownSettings={item.markdown_settings}
            queries={queries}
          />
        );
      }

      let xsSize;
      if (item.size < 7) {
        xsSize = item.size * 2;
      } else {
        xsSize = item.size;
      }
      items.push(
        <Grid
          item
          // We allow index in keys here because the config isn't reloaded, and as such elements
          // in the config will never change.
          // eslint-disable-next-line react/no-array-index-key
          key={index}
          lg={item.size}
          md={item.size}
          xl={item.size}
          xs={xsSize}
        >
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
        <title>Dashboard | Seizu</title>
      </Helmet>
      <Box
        sx={{
          backgroundColor: 'background.default',
          minHeight: '100%',
          py: 3
        }}
      >
        <Grid container>{rows}</Grid>
      </Box>
    </>
  );
}

export default Dashboard;
