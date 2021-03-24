import react from "react";
import {Button, Card, PageHeader, Typography} from "antd";
import Layout, {Content, Footer, Header} from "antd/lib/layout/layout";
import {FontColorsOutlined} from "@ant-design/icons";
import "./styles.css";
// import Title from "antd/lib/skeleton/Title";
import {useAuth0} from "@auth0/auth0-react";
// const { Header, Content, Footer } = Layout;

const {Title} = Typography;

function Landing() {
  const {loginWithRedirect} = useAuth0();

  return (
    <Layout className="fullpage">
      {/* <PageHeader className = 'site-page-header' title = 'InterIIT Bosch Traffic Sign Detector' textAlign='center'>

            </PageHeader> */}
      <Header classname="site-layout-subheader-background">
        <Title level={2} style={{color: "white", padding: "10px", textAlign: "center"}}>
          InterIIT Bosch Traffic Sign Recogniser
        </Title>
      </Header>

      <Content className="site-layout-content">
        <div class="center" align="center">
          <Card
            title={<Title level={3}>Continue with OAuth0</Title>}
            style={{width: "40vh", alignItems: "center", height: "40vh"}}
            hoverable="True"
          >
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: "10vh",
              }}
            >
              <Button
                onClick={() => loginWithRedirect()}
                type="primary"
                size="large"
                style={{align: "center"}}
              >
                Login
              </Button>{" "}
              <br />
            </div>
          </Card>
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
