import styled from 'styled-components';

const Card = styled.div`
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index:100;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  position: fixed;
  height: 35rem;
  width: 35rem;
  left: calc((100% - 35rem) / 2) ;
  top: calc((100% - 35rem) / 2) ;
  z-index: 100;
  border-radius: 20px;
`;

const Form = styled.div`
  display: flex;
  flex-direction: column;
  width: 50%;
`;

const Input = styled.input`
  padding: 1rem;
  border: 1px solid #999;
  margin-bottom: 1rem;
  font-size: 0.8rem;
`;

const Button = styled.button`
  background: linear-gradient(to bottom, #6371c7, #5563c1);
  border-color: #3f4eae;
  border-radius: 3px;
  padding: 1rem;
  color: white;
  font-weight: 700;
  width: 50%;
  margin: 0 auto;
  margin-bottom: 1rem;
  font-size: 0.8rem;
`;

const Error = styled.div`
  background-color: red;
`;

export { Form, Input, Button, Card, Error };
