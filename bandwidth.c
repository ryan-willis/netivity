#include <ifaddrs.h>
#include <net/if.h>
#include <string.h>

struct params {
  uint64_t last_out;
  uint64_t last_in;
  uint64_t net_in;
  uint64_t net_out;
  char name[16];
};

void get_bandwidth(struct params *p) {
  struct ifaddrs *ifa_list = 0, *ifa;
  if (getifaddrs(&ifa_list) == -1)
    goto done;
  for (ifa = ifa_list; ifa; ifa = ifa->ifa_next) {
    if (AF_LINK != ifa->ifa_addr->sa_family)
      continue;
    if (!(ifa->ifa_flags & IFF_UP) && !(ifa->ifa_flags & IFF_RUNNING))
      continue;
    if (ifa->ifa_data == 0)
      continue;
    if (strcmp(p->name, ifa->ifa_name) == 0) {
      struct if_data *ifd = (struct if_data *)ifa->ifa_data;
      if (p->last_in > 0)
        p->net_in = ifd->ifi_ibytes - p->last_in;
      if (p->last_out > 0)
        p->net_out = ifd->ifi_obytes - p->last_out;
      p->last_in = ifd->ifi_ibytes;
      p->last_out = ifd->ifi_obytes;
    }
  }
done:
  freeifaddrs(ifa_list);
}

#ifdef DEBUG
int main() {
  struct params p = {0, 0, 0, 0};
  strcpy(p.name, "en0");
  get_bandwidth(&p);
  return 0;
}
#endif