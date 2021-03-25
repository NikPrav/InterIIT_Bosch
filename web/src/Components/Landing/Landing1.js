import react from "react";
import {Button, PageHeader, Typography} from "antd";
import Layout, {Content, Footer, Header, Card} from "antd/lib/layout/layout";
import {useAuth0} from "@auth0/auth0-react";
import "./styles.css";
// import Title from "antd/lib/skeleton/Title";
const {Title} = Typography;
// const { Header, Content, Footer } = Layout;

function Landing() {
  const {loginWithRedirect} = useAuth0();
  return (
    <Layout className="fullpage" style={{textAlign: "center"}}>
      {/* <PageHeader className = 'site-page-header' title = 'InterIIT Bosch Traffic Sign Detector' textAlign='center'>

            </PageHeader> */}
      <Header classname="site-leayout-subheader-background">
        <Title level={2} style={{color: "white", padding: "10px"}}>
          InterIIT Bosch Traffic Sign Recogniser
        </Title>
      </Header>

      <Content className="site-layout-content" style={{textAlign: "center"}}>
        <div class="center">
          <Card
            title={<Title level={3}>Continue with OAuth0</Title>}
            style={{width: "40vh", alignItems: "center", height: "40vh"}}
            hoverable="True"
          >
            <Button onClick={() => loginWithRedirect()} type="primary" href="/home" size="large">
              Login
            </Button>
            <br />
          </Card>
          <div style={{textAlign: "center"}}>
            Press button to login, and add start training to make it look cool.
          </div>
        </div>
      </Content>

      <Footer className="site-layout-footer">
        <div>
          <a style={{float: "left"}} href="https://github.com/npalladium/InterIIT-Bosch">
            Github link
          </a>
          <b style={{float: "right"}}>IIT Hyderabad,2021</b>
        </div>
      </Footer>
    </Layout>
  );
}

export default Landing;
