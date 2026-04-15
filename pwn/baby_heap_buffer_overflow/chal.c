#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <malloc.h>

struct object_t {
  char content[64];
};

struct vtable_t {
  void (*read)(struct object_t*);
  void (*write)(struct object_t*);
};


void read_name(struct object_t* object) {
  fgets(object->content,0x64,stdin);
}

void write_name(struct object_t* object) {
  printf("%s\n",object->content);
}


int getcmd() {
  int cmd = 0;
  scanf("%d",&cmd);
  getchar();
  return cmd;
}

void menu(){
  puts("");
  puts("1 - read");
  puts("2 - write");
  puts("3 - exit");
  printf("> ");
}

int main() {
  setbuf(stdin,NULL);
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);

  struct object_t* object = malloc(sizeof(struct object_t));
  struct vtable_t* vtable = malloc(sizeof(struct vtable_t));

  vtable->read = read_name;
  vtable->write = write_name;

  system("echo Baby Heap Overflow");
  while(1) {
    menu();
    int cmd = getcmd();
    switch(cmd) {
      case 1:
	vtable->read(object);
	break;
      case 2:
	vtable->write(object);
	break;
      case 3:
  	free(object);
  	free(vtable);
	puts("bye!");
	return 0;
      default:
	puts("unknown cmd");
	break;
    }
  }
  return 0;
}