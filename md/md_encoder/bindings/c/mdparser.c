#include "../mdparser.h"
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>

int main()
{
    void *handle = dlopen("./libmdencoder.so", RTLD_LAZY);

    init_proto_generator = dlsym(handle, "init_proto_generator");
    set_threshold = dlsym(handle, "set_threshold");
    generate_proto = dlsym(handle, "generate_proto");
    free_proto = dlsym(handle, "free_proto");
    free_proto_vec = dlsym(handle, "free_proto_vec");

    char input[] = "# This is title\n## This is title2";

    // uint32_t r = init_threadpool(32);
    CProtoGenerator *g = init_proto_generator(1000);
    const CProtoVec *u = generate_proto(g, input);
    printf("len: %d\n", u->len);
    for (int i = 0; i < u->len; i++)
    {
        printf("\tlen: %d\n", u->data[i]->len);
        for (int j = 0; j < u->data[i]->len; j++)
        {
            printf("%d ", u->data[i]->data[j]);
        }
    }
    free_proto_vec(u);
    dlclose(handle);
}