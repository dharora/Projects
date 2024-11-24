import socket
import struct
import binascii

def build_dns_request(domain, record_type):
    # DNS header: ID, QR (0 for query), QDCOUNT (number of questions)
    dns_id = 1234  # You can choose any ID
    flags = 0b0000000100000000  # QR=0 (query), Opcode=0 (standard query), AA=0, TC=0, RD=1 (recursion desired)
    qd_count = 1  # Number of questions

    # DNS question section format: QNAME, QTYPE, QCLASS
    qname = encode_domain(domain)
    qtype = get_record_type_code(record_type)
    qclass = 1  # IN (Internet)

    # Pack the DNS header and question section
    dns_header = struct.pack('!HHHHHH', dns_id, flags, qd_count, 0, 0, 0)
    dns_question = struct.pack('!%dsHH' % len(qname), qname, qtype, qclass)

    # Combine header and question to create the DNS request
    dns_request = dns_header + dns_question

    return dns_request

def encode_domain(domain):
    labels = domain.split('.')
    encoded_labels = [struct.pack('!B', len(label)) + label.encode() for label in labels]
    return b''.join(encoded_labels) + b'\x00'  # Null-terminated

def get_record_type_code(record_type):
    if record_type.upper() == 'A':
        return 1  # IPv4 address
    elif record_type.upper() == 'AAAA':
        return 28  # IPv6 address
    else:
        raise ValueError("Invalid record type. Use 'A' for IPv4 or 'AAAA' for IPv6.")

def unpack_dns_response(response):
    # Unpack DNS header
    dns_id, flags, qd_count, an_count, ns_count, ar_count = struct.unpack('!HHHHHH', response[:12])

    # Extract answers from the response
    answers = parse_dns_answers(response[12:], an_count)

    return {
        'ID': dns_id,
        'Flags': flags,
        'QDCOUNT': qd_count,
        'ANCOUNT': an_count,
        'NSCOUNT': ns_count,
        'ARCOUNT': ar_count,
        'ANSWERS': answers
    }

def parse_dns_answers(answer_section, count):
    answers = []

    # Iterate over each answer in the answer section
    offset = 0
    for _ in range(count):
        name, offset = read_domain(answer_section, offset)
        answer_type, answer_class, answer_ttl, answer_rd_length = struct.unpack('!HHIH', answer_section[offset: offset + 10])
        offset += 10

        # Extract IP address from answer data
        ip_address = extract_ip_from_answer(answer_type, answer_section[offset: offset + answer_rd_length])
        offset += answer_rd_length

        answers.append({
            'NAME': name,
            'TYPE': answer_type,
            'CLASS': answer_class,
            'TTL': answer_ttl,
            'RD_LENGTH': answer_rd_length,
            'IP_ADDRESS': ip_address
        })

    return answers

def extract_ip_from_answer(answer_type, answer_data):
    if answer_type == 1:  # Type 1 corresponds to A (IPv4 address) records
        return '.'.join(str(byte) for byte in answer_data)
    elif answer_type == 28:  # Type 28 corresponds to AAAA (IPv6 address) records
        return ':'.join(f'{byte:02x}' for byte in answer_data)
    else:
        return None

def read_domain(response, offset):
    labels = []
    while True:
        label_length = struct.unpack('!B', response[offset: offset + 1])[0]
        offset += 1
        if label_length == 0:
            break
        labels.append(response[offset: offset + label_length].decode())
        offset += label_length
    return '.'.join(labels), offset

def send_dns_request(dns_request, dns_resolver='198.41.0.4', dns_port=53):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(dns_request, (dns_resolver, dns_port))
        response, _ = s.recvfrom(1024)
    return response

if __name__ == "__main__":  
    # Example usage for IPv4
    domain_to_query_ipv4 = "tmz.com"
    ipv4_dns_request = build_dns_request(domain_to_query_ipv4, 'A')
    ipv4_dns_response = send_dns_request(ipv4_dns_request)
    unpacked_ipv4_dns_response = unpack_dns_response(ipv4_dns_response)


    # Example usage for IPv6
    domain_to_query_ipv6 = "tmz.com"
    ipv6_dns_request = build_dns_request(domain_to_query_ipv6, 'AAAA')
    ipv6_dns_response = send_dns_request(ipv6_dns_request)
    unpacked_ipv6_dns_response = unpack_dns_response(ipv6_dns_response)

    # Print the unpacked information
    print("IPv4 DNS Request")
    print(ipv4_dns_request)

    print("IPv4 DNS Response:")
    print(binascii.hexlify(ipv4_dns_response))
    print("Unpacked IPv4 DNS Response:")
    print(unpacked_ipv4_dns_response)

    print("IPv6 DNS Request")
    print(ipv6_dns_request)
    print("\nIPv6 DNS Response:")
    print(binascii.hexlify(ipv6_dns_response))
    print("Unpacked IPv6 DNS Response:")
    print(unpacked_ipv6_dns_response)
