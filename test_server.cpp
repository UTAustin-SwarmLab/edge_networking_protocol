#include <string>
#include <zmq.hpp>

int main()
{
  printf("Hello World!\n");
   zmq::context_t context(1);
   zmq::socket_t sock(context, zmq::socket_type::req);
   sock.bind("tcp://*:5555");
  //  while (true) {
  //   //  zmq::message
  //  }
   const std::string_view m = "Hello, world";
   sock.send(zmq::buffer(m), zmq::send_flags::dontwait);
  printf("Hello World!\n");
}